# Quick Fix for 500 Error

## Problem
Getting "Request failed with status code 500" when uploading a video.

## Solution

The 500 error is likely due to missing Python dependencies. Install them:

### Step 1: Install Required Dependencies

```bash
cd hr-video-analyzer
pip install -r requirements.txt
```

### Step 2: Verify Installation

Check if OpenCV is installed (required for video processing):
```bash
python3 -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

If you get an error, install it:
```bash
pip install opencv-python
```

### Step 3: Restart the Server

After installing dependencies, restart your FastAPI server:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
uvicorn app:app --reload
```

### Step 4: Try Uploading Again

Upload a video and check if the error is resolved.

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'cv2'"
**Solution**: `pip install opencv-python`

### Issue: "ModuleNotFoundError: No module named 'numpy'"
**Solution**: `pip install numpy`

### Issue: "ModuleNotFoundError: No module named 'torch'"
**Solution**: `pip install torch torchvision`

Note: PyTorch is optional for facial expression analysis. The system will use a rule-based fallback if PyTorch is not available.

## Check Server Logs

If the error persists, check your server terminal/logs for detailed error messages. The error will show which specific module is missing.

## Full Installation

For a complete installation of all dependencies:

```bash
cd hr-video-analyzer
pip install -r requirements.txt
```

This installs:
- FastAPI and Uvicorn (web server)
- OpenCV (video processing)
- NumPy (numerical operations)
- PyTorch (optional, for ML features)
- And other dependencies

