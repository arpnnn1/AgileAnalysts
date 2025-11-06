# Fixing Network Error

## Problem
Getting "Network error" or "Cannot connect to server" when uploading/analyzing videos.

## Common Causes & Solutions

### 1. Backend Server Not Running

**Symptom**: Network error, connection refused

**Solution**: Start the FastAPI backend server

```bash
cd hr-video-analyzer
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The server should start and show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Wrong Port

**Check**: The frontend proxy is configured for `http://localhost:8000`

**Verify**: Make sure your backend is running on port 8000:
```bash
# Check if port 8000 is in use
lsof -i :8000
```

If using a different port, update `frontend/package.json`:
```json
"proxy": "http://localhost:YOUR_PORT"
```

### 3. Frontend Not Using Proxy

**If running frontend separately** (not through FastAPI):

The frontend needs to proxy requests to the backend. Make sure:

1. **Development mode** (npm start):
   - Proxy is configured in `package.json`: `"proxy": "http://localhost:8000"`
   - Frontend runs on `http://localhost:3000`
   - Backend runs on `http://localhost:8000`

2. **Production mode** (served by FastAPI):
   - Build the frontend: `cd frontend && npm run build`
   - FastAPI serves the built files automatically

### 4. CORS Issues

**Symptom**: CORS error in browser console

**Solution**: The backend already has CORS configured. If issues persist, check:
- Backend is running
- Frontend URL matches CORS allowed origins in `app.py`

### 5. Firewall/Network Issues

**Check**: 
- No firewall blocking port 8000
- Both frontend and backend are on same machine (for localhost)

## Quick Diagnostic Steps

1. **Check if backend is running**:
   ```bash
   curl http://localhost:8000/
   ```
   Should return: `{"status":"ok","message":"HR Video Analyzer is running"}`

2. **Check backend logs**:
   Look at the terminal where you started `uvicorn`. Any errors there?

3. **Check browser console**:
   Open browser DevTools (F12) → Console tab
   Look for detailed error messages

4. **Check Network tab**:
   Open browser DevTools → Network tab
   Try uploading again and see what request fails

## Typical Setup

### Terminal 1 - Backend:
```bash
cd hr-video-analyzer
uvicorn app:app --reload --port 8000
```

### Terminal 2 - Frontend (if running separately):
```bash
cd hr-video-analyzer/frontend
npm start
```

Then open: `http://localhost:3000`

## Alternative: Run Everything Through FastAPI

If you want to avoid proxy issues:

1. Build the frontend:
   ```bash
   cd hr-video-analyzer/frontend
   npm run build
   ```

2. Start only the backend:
   ```bash
   cd hr-video-analyzer
   uvicorn app:app --reload --port 8000
   ```

3. Open: `http://localhost:8000`

FastAPI will serve both the API and the React app.

## Still Having Issues?

1. Check server terminal for error messages
2. Check browser console (F12) for detailed errors
3. Verify all dependencies are installed: `pip install -r requirements.txt`
4. Try accessing the API directly: `http://localhost:8000/` in browser

