import React, { useState } from 'react';
import './ResultsDisplay.css';

const ResultsDisplay = ({ results }) => {
  const [selectedFrame, setSelectedFrame] = useState(null);

  if (!results) return null;

  const { annotated_frames = [], results: analysisResults = {}, results_file, uploaded_file } = results;

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Analysis Results</h2>
        {results_file && (
          <a href={results_file} target="_blank" rel="noopener noreferrer" className="results-link">
            View Full Results JSON
          </a>
        )}
      </div>

      <div className="results-stats">
        <div className="stat-card">
          <div className="stat-value">{annotated_frames.length}</div>
          <div className="stat-label">Frames Analyzed</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {Object.values(analysisResults).reduce((sum, faces) => sum + faces.length, 0)}
          </div>
          <div className="stat-label">Total Faces Detected</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {Object.values(analysisResults).filter(faces => faces.length > 0).length}
          </div>
          <div className="stat-label">Frames with Faces</div>
        </div>
      </div>

      {annotated_frames.length > 0 && (
        <div className="frames-section">
          <h3>Annotated Frames</h3>
          <div className="frames-grid">
            {annotated_frames.map((frameUrl, index) => {
              const frameName = frameUrl.split('/').pop();
              const frameKey = frameName.replace('annot_', '').replace('.jpg', '');
              const faces = analysisResults[frameKey] || [];
              
              return (
                <div
                  key={index}
                  className={`frame-item ${selectedFrame === index ? 'selected' : ''}`}
                  onClick={() => setSelectedFrame(selectedFrame === index ? null : index)}
                >
                  <img
                    src={frameUrl}
                    alt={`Frame ${index + 1}`}
                    className="frame-image"
                    loading="lazy"
                  />
                  <div className="frame-overlay">
                    <div className="frame-info">
                      <span className="frame-number">Frame {index + 1}</span>
                      <span className="face-count">
                        {faces.length} {faces.length === 1 ? 'face' : 'faces'}
                      </span>
                    </div>
                  </div>
                  {selectedFrame === index && faces.length > 0 && (
                    <div className="frame-details">
                      <h4>Face Detection Details:</h4>
                      <ul>
                        {faces.map((face, faceIndex) => (
                          <li key={faceIndex}>
                            Face {faceIndex + 1}: Position ({face.x}, {face.y}), 
                            Size {face.w}×{face.h}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {uploaded_file && (
        <div className="uploaded-video-section">
          <h3>Original Video</h3>
          <video controls className="uploaded-video">
            <source src={uploaded_file} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;

