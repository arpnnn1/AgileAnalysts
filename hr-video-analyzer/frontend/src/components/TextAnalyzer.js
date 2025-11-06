import React, { useState } from 'react';
import axios from 'axios';
import './TextAnalyzer.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

const TextAnalyzer = ({ onAnalysisSuccess, onAnalysisError, onLoading, loading }) => {
  const [text, setText] = useState('');
  const [placeholder] = useState('Enter text to analyze sentiment...\n\nExample: "I love this product! It works perfectly and makes my life so much easier."');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!text || !text.trim()) {
      alert('Please enter some text to analyze');
      return;
    }

    onLoading(true);
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/analyze-sentiment/`,
        { text: text.trim() },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      onAnalysisSuccess(response.data);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Analysis failed';
      onAnalysisError(new Error(errorMessage));
    } finally {
      onLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
    onAnalysisSuccess(null);
  };

  return (
    <div className="text-analyzer-container">
      <form onSubmit={handleSubmit} className="text-analyzer-form">
        <div className="form-group">
          <label htmlFor="textInput" className="text-label">
            Enter Text for Sentiment Analysis
          </label>
          <textarea
            id="textInput"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={placeholder}
            disabled={loading}
            className="text-input"
            rows="8"
          />
          <div className="text-info">
            <span className="char-count">{text.length} characters</span>
            <span className="word-count">{text.trim() ? text.trim().split(/\s+/).length : 0} words</span>
          </div>
        </div>

        <div className="button-group">
          <button
            type="submit"
            disabled={!text.trim() || loading}
            className="analyze-button"
          >
            {loading ? 'Analyzing...' : 'Analyze Sentiment'}
          </button>
          {text && (
            <button
              type="button"
              onClick={handleClear}
              disabled={loading}
              className="clear-button"
            >
              Clear
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default TextAnalyzer;

