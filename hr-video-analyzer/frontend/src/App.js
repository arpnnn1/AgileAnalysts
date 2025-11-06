import React, { useState } from 'react';
import './App.css';
import VideoUpload from './components/VideoUpload';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUploadSuccess = (data) => {
    setResults(data);
    setError(null);
  };

  const handleUploadError = (err) => {
    setError(err.message || 'An error occurred during upload');
    setResults(null);
  };

  const handleLoading = (isLoading) => {
    setLoading(isLoading);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>HR Video Analyzer</h1>
        <p>Upload a video to run face detection and analysis</p>
      </header>
      <main className="App-main">
        <VideoUpload
          onUploadSuccess={handleUploadSuccess}
          onUploadError={handleUploadError}
          onLoading={handleLoading}
          loading={loading}
        />
        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}
        {results && <ResultsDisplay results={results} />}
      </main>
    </div>
  );
}

export default App;

