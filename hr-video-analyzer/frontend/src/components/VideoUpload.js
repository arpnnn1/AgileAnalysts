import React, { useState } from 'react';
import axios from 'axios';
import './VideoUpload.css';

// Use relative URLs by default (works with proxy in dev and when served from FastAPI)
// Set REACT_APP_API_URL environment variable to override (e.g., for different domain)
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

const VideoUpload = ({ onUploadSuccess, onUploadError, onLoading, loading }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [step, setStep] = useState(30);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type.startsWith('video/')) {
        setSelectedFile(file);
      } else {
        alert('Please select a video file');
        e.target.value = '';
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      alert('Please select a video file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    onLoading(true);
    try {
      const response = await axios.post(
        `${API_BASE_URL}/upload/?step=${step}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      onUploadSuccess(response.data);
    } catch (err) {
      // Extract detailed error message from response
      let errorMessage = 'Upload failed';
      if (err.response?.data) {
        if (err.response.data.message) {
          errorMessage = err.response.data.message;
        } else if (err.response.data.error) {
          errorMessage = err.response.data.error;
        } else if (err.response.data.detail) {
          errorMessage = err.response.data.detail;
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      onUploadError(new Error(errorMessage));
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="video-upload-container">
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-group">
          <label htmlFor="fileInput" className="file-label">
            <span className="file-label-text">Select Interview Video</span>
            <input
              type="file"
              id="fileInput"
              accept="video/*"
              onChange={handleFileChange}
              disabled={loading}
              className="file-input"
            />
          </label>
          {selectedFile && (
            <div className="file-info">
              <p>Selected: <strong>{selectedFile.name}</strong></p>
              <p>Size: {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
            </div>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="stepInput" className="step-label">
            Extract Step (frames):
            <input
              type="number"
              id="stepInput"
              value={step}
              onChange={(e) => setStep(parseInt(e.target.value) || 30)}
              min="1"
              disabled={loading}
              className="step-input"
            />
          </label>
          <small className="step-hint">
            Extract every Nth frame (lower = more frames, slower processing). Audio will be transcribed automatically.
          </small>
        </div>

        <button
          type="submit"
          disabled={!selectedFile || loading}
          className="upload-button"
        >
          {loading ? 'Processing Video & Transcribing Audio...' : 'Upload & Analyze Interview'}
        </button>
      </form>
    </div>
  );
};

export default VideoUpload;

