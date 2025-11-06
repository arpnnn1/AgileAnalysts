from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid

import video_processor

UPLOAD_DIR = "uploads"

app = FastAPI(title="HR Video Analyzer (demo)")

# Mount a static files directory so uploaded and annotated files are reachable
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "HR Video Analyzer is running"}


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

    # Collect annotated frame URLs (served under /static)
    annotated_dir = os.path.join(work_dir, "annotated")
    annotated_urls = []
    if os.path.exists(annotated_dir):
        for f in sorted(os.listdir(annotated_dir)):
            rel = os.path.join(uid, "annotated", f).replace("\\", "/")
            annotated_urls.append(f"/static/{rel}")

    # Results file path (serveable via /static as well)
    results_rel = os.path.join(uid, "results.json").replace("\\", "/")
    results_url = f"/static/{results_rel}"

    return JSONResponse({
        "results_file": results_url,
        "results": results,
        "annotated_frames": annotated_urls,
        "uploaded_file": f"/static/{save_name}",
    })
