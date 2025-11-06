import React, { useState } from 'react';
import './App.css';
import VideoUpload from './components/VideoUpload';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  // Video analysis state
  const [videoResults, setVideoResults] = useState(null);
  const [videoLoading, setVideoLoading] = useState(false);
  const [videoError, setVideoError] = useState(null);

  // Video handlers
  const handleUploadSuccess = (data) => {
    setVideoResults(data);
    setVideoError(null);
  };

  const handleUploadError = (err) => {
    setVideoError(err.message || 'An error occurred during upload');
    setVideoResults(null);
  };

  const handleVideoLoading = (isLoading) => {
    setVideoLoading(isLoading);
  };

  return (
    <div className="App" style={{ position: 'relative', zIndex: 1 }}>
      <header className="App-header" style={{ position: 'relative', zIndex: 2 }}>
        <h1>HR Interview Analytics Platform</h1>
        <p>Video Analysis, Transcription & Candidate Evaluation</p>
      </header>
      <main className="App-main">
        <VideoUpload
          onUploadSuccess={handleUploadSuccess}
          onUploadError={handleUploadError}
          onLoading={handleVideoLoading}
          loading={videoLoading}
        />
        {videoError && (
          <div className="error-message">
            <p>Error: {videoError}</p>
          </div>
        )}
        {videoResults && <ResultsDisplay results={videoResults} />}
      </main>
    </div>
  );
}

export default App;

