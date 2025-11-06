# Quick Setup Guide

## Backend Setup

1. **Activate virtual environment:**
```bash
cd hr-video-analyzer
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies (if not already installed):**
```bash
pip install -r requirements.txt
```

3. **Run the FastAPI backend:**
```bash
uvicorn app:app --reload --port 8000
```

## Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start React development server:**
```bash
npm start
```

The React app will open at `http://localhost:3000` and will proxy API requests to the backend at `http://localhost:8000`.

## Production Build

To build and serve the React app from FastAPI:

1. **Build the React app:**
```bash
cd frontend
npm run build
```

2. **Start FastAPI (it will automatically serve the React build):**
```bash
cd ..
uvicorn app:app --port 8000
```

3. **Access the application at:** `http://localhost:8000`

## Notes

- The backend API is available at `http://localhost:8000`
- In development, React runs on port 3000 and proxies to port 8000
- In production, React is served directly from FastAPI at port 8000
- Uploaded files and results are stored in the `uploads/` directory
- CORS is enabled for localhost:3000 and localhost:8000

