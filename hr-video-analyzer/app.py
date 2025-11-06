from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
import shutil
import os
import uuid

import video_processor

UPLOAD_DIR = "uploads"
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(__file__), "frontend", "build")

app = FastAPI(title="HR Video Analyzer (demo)")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # React dev server and production
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
async def upload_video(file: UploadFile = File(...), step: int = 30):
    """Receive an uploaded video, process it (frame extraction + face detection), and return results."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    uid = str(uuid.uuid4())
    # Save uploaded file into uploads/ for easy serving if desired
    save_name = f"{uid}_{file.filename}"
    save_path = os.path.join(UPLOAD_DIR, save_name)
    with open(save_path, "wb") as out_file:
        shutil.copyfileobj(file.file, out_file)

    # Process video (frames + analysis)
    work_dir = os.path.join(UPLOAD_DIR, uid)
    results_path, results = video_processor.process_video(save_path, step=step, work_dir=work_dir)

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

    return JSONResponse({
        "results_file": results_url,
        "results": results,
        "annotated_frames": annotated_urls,
        "uploaded_file": f"/uploads/{save_name}",
    })
