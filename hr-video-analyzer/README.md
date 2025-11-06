# HR Video Analyzer

A full-stack application for analyzing videos with face detection capabilities. The backend is built with FastAPI and the frontend is built with React.

## Features

- Upload video files for analysis
- Automatic frame extraction from videos
- Face detection using OpenCV's Haar Cascade classifier
- Visual display of annotated frames with detected faces
- Interactive results dashboard

## Project Structure

```
hr-video-analyzer/
├── app.py                 # FastAPI backend application
├── video_processor.py     # Video processing and face detection logic
├── requirements.txt       # Python dependencies
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── App.js        # Main React component
│   │   ├── components/   # React components
│   │   │   ├── VideoUpload.js
│   │   │   └── ResultsDisplay.js
│   │   └── ...
│   └── package.json      # Node.js dependencies
└── uploads/              # Directory for uploaded videos and results
```

## Setup Instructions

### Prerequisites

- Python 3.8+ 
- Node.js 14+ and npm
- Virtual environment (recommended)

### Backend Setup

1. **Create and activate a virtual environment:**

```bash
cd hr-video-analyzer
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the FastAPI backend:**

```bash
uvicorn app:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory:**

```bash
cd frontend
```

2. **Install Node.js dependencies:**

```bash
npm install
```

3. **Start the React development server:**

```bash
npm start
```

The frontend will be available at `http://localhost:3000` and will automatically proxy API requests to the backend.

### Production Build

To build the React app for production and serve it from FastAPI:

1. **Build the React app:**

```bash
cd frontend
npm run build
```

2. **The FastAPI app will automatically serve the built React app** when you access `http://localhost:8000` after building.

## Usage

### Development Mode

1. Start the FastAPI backend on port 8000
2. Start the React development server on port 3000
3. Open `http://localhost:3000` in your browser
4. Upload a video file and configure the frame extraction step
5. View the analysis results with annotated frames

### Production Mode

1. Build the React frontend: `cd frontend && npm run build`
2. Start the FastAPI backend: `uvicorn app:app --port 8000`
3. Access the application at `http://localhost:8000`

## API Endpoints

- `GET /` - API status or serves React app (if built)
- `GET /ui` - Legacy HTML upload page
- `POST /upload/` - Upload and analyze a video file
  - Parameters:
    - `file`: Video file (multipart/form-data)
    - `step`: Frame extraction step (default: 30)

## Technologies Used

### Backend
- FastAPI - Modern Python web framework
- OpenCV - Computer vision library for face detection
- Uvicorn - ASGI server

### Frontend
- React - JavaScript UI library
- Axios - HTTP client for API requests
- CSS3 - Styling

## Notes

- The application processes videos by extracting frames at specified intervals
- Face detection uses OpenCV's Haar Cascade classifier
- Uploaded videos and results are stored in the `uploads/` directory
- CORS is enabled for development (localhost:3000 and localhost:8000)

