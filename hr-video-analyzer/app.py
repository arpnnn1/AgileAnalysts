from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
import uuid

import video_processor

# Optional text analyzer (for text sentiment analysis feature)
# Catch all exceptions since there may be dependency issues (NumPy/SciPy version conflicts)
try:
    import text_analyzer
    TEXT_ANALYZER_AVAILABLE = True
    analyzer = text_analyzer.TextAnalyzer()
except (ImportError, ValueError, Exception) as e:
    TEXT_ANALYZER_AVAILABLE = False
    text_analyzer = None
    analyzer = None
    print(f"Warning: Text analyzer not available: {type(e).__name__}: {e}")

UPLOAD_DIR = "uploads"
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(__file__), "frontend", "build")

app = FastAPI(title="HR Video Analyzer (demo)")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000"],  # React dev server and production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount a static files directory so uploaded and annotated files are reachable
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Serve React build directory (includes static assets)
if os.path.exists(FRONTEND_BUILD_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_BUILD_DIR), name="react-build")


@app.get("/")
def read_root():
    """Serve React app if built, otherwise return API status."""
    index_path = os.path.join(FRONTEND_BUILD_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "ok", "message": "HR Video Analyzer is running"}


@app.exception_handler(404)
async def catch_all_handler(request: Request, exc: HTTPException):
    """Catch-all handler to serve React app for non-API routes."""
    # Only serve React app for non-API routes
    if not request.url.path.startswith(("/api", "/uploads", "/upload", "/ui")):
        index_path = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
    raise exc


@app.get("/ui")
def upload_page():
    """A tiny HTML page to upload videos from a browser."""
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return HTMLResponse(open(index_path, "r").read())
    return HTMLResponse("<html><body><h3>No UI found</h3></body></html>")


@app.post("/upload/")
async def upload_video(file: UploadFile = File(...), step: int = 30, transcribe: bool = True):
    """Receive an uploaded video, process it (frame extraction + face detection + transcription + evaluation), and return results."""
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        uid = str(uuid.uuid4())
        # Save uploaded file into uploads/ for easy serving if desired
        save_name = f"{uid}_{file.filename}"
        save_path = os.path.join(UPLOAD_DIR, save_name)
        with open(save_path, "wb") as out_file:
            shutil.copyfileobj(file.file, out_file)

        # Process video (frames + analysis + transcription + evaluation)
        work_dir = os.path.join(UPLOAD_DIR, uid)
        results_path, results = video_processor.process_video(save_path, step=step, work_dir=work_dir, transcribe_audio=transcribe)
    except ImportError as e:
        # Handle missing dependencies gracefully
        import traceback
        error_details = traceback.format_exc()
        print(f"Import error during video processing: {e}")
        print(f"Error details: {error_details}")
        return JSONResponse(
            {
                "error": str(e),
                "error_type": "ImportError",
                "message": f"Missing required dependency: {str(e)}. Please install required packages: pip install -r requirements.txt"
            },
            status_code=500
        )
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing video: {e}")
        print(f"Error details: {error_details}")
        return JSONResponse(
            {
                "error": str(e),
                "error_type": type(e).__name__,
                "message": "Video processing failed. Check server logs for details.",
                "traceback": error_details if "ImportError" in str(e) or "ModuleNotFoundError" in str(e) else None
            },
            status_code=500
        )

    # Collect annotated frame URLs (served under /uploads)
    annotated_dir = os.path.join(work_dir, "annotated")
    annotated_urls = []
    if os.path.exists(annotated_dir):
        for f in sorted(os.listdir(annotated_dir)):
            rel = os.path.join(uid, "annotated", f).replace("\\", "/")
            annotated_urls.append(f"/uploads/{rel}")

    # Results file path (serveable via /uploads as well)
    results_rel = os.path.join(uid, "results.json").replace("\\", "/")
    results_url = f"/uploads/{results_rel}"

    # Extract separate components for easier frontend access
    frame_analysis = results.get("frame_analysis", {})
    transcription = results.get("transcription")
    evaluation = results.get("evaluation")
    facial_expression_analysis = results.get("facial_expression_analysis")

    return JSONResponse({
        "results_file": results_url,
        "results": frame_analysis,  # Keep for backward compatibility
        "frame_analysis": frame_analysis,
        "transcription": transcription,
        "evaluation": evaluation,
        "facial_expression_analysis": facial_expression_analysis,
        "annotated_frames": annotated_urls,
        "uploaded_file": f"/uploads/{save_name}",
    })


# Pydantic models for sentiment analysis
class TextAnalysisRequest(BaseModel):
    text: str


class BatchTextAnalysisRequest(BaseModel):
    texts: List[str]


@app.post("/api/analyze-sentiment/")
async def analyze_sentiment(request: TextAnalysisRequest):
    """Analyze sentiment of a single text."""
    if not TEXT_ANALYZER_AVAILABLE or analyzer is None:
        return JSONResponse(
            {"error": "Text analyzer not available. Install dependencies: pip install textblob vaderSentiment nltk"},
            status_code=503
        )
    try:
        result = analyzer.analyze(request.text)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(
            {"error": str(e), "text": request.text},
            status_code=500
        )


@app.post("/api/analyze-sentiment-batch/")
async def analyze_sentiment_batch(request: BatchTextAnalysisRequest):
    """Analyze sentiment of multiple texts."""
    if not TEXT_ANALYZER_AVAILABLE or analyzer is None:
        return JSONResponse(
            {"error": "Text analyzer not available. Install dependencies: pip install textblob vaderSentiment nltk"},
            status_code=503
        )
    try:
        results = analyzer.analyze_batch(request.texts)
        return JSONResponse({"results": results, "count": len(results)})
    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )
