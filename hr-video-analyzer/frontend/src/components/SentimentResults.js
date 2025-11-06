import React from 'react';
import './SentimentResults.css';

const SentimentResults = ({ results }) => {
  if (!results || results.error) {
    return (
      <div className="sentiment-results-container">
        <div className="error-message">
          {results?.error || 'No results to display'}
        </div>
      </div>
    );
  }

  const { overall_sentiment, textblob, vader, text, text_length, word_count } = results;

  const getSentimentColor = (label) => {
    switch (label.toLowerCase()) {
      case 'positive':
        return '#4caf50';
      case 'negative':
        return '#f44336';
      case 'neutral':
        return '#ff9800';
      default:
        return '#757575';
    }
  };

  const getSentimentEmoji = (label) => {
    switch (label.toLowerCase()) {
      case 'positive':
        return '😊';
      case 'negative':
        return '😞';
      case 'neutral':
        return '😐';
      default:
        return '🤔';
    }
  };

  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  return (
    <div className="sentiment-results-container">
      <div className="results-header">
        <h2>Sentiment Analysis Results</h2>
      </div>

      {/* Overall Sentiment */}
      <div className="overall-sentiment-card">
        <div className="sentiment-badge" style={{ backgroundColor: getSentimentColor(overall_sentiment.label) }}>
          <span className="sentiment-emoji">{getSentimentEmoji(overall_sentiment.label)}</span>
          <div className="sentiment-info">
            <div className="sentiment-label">{overall_sentiment.label.toUpperCase()}</div>
            <div className="sentiment-confidence">
              Confidence: {formatPercentage(overall_sentiment.confidence)}
            </div>
          </div>
        </div>
      </div>

      {/* Text Stats */}
      <div className="text-stats">
        <div className="stat-item">
          <div className="stat-value">{text_length}</div>
          <div className="stat-label">Characters</div>
        </div>
        <div className="stat-item">
          <div className="stat-value">{word_count}</div>
          <div className="stat-label">Words</div>
        </div>
      </div>

      {/* Analysis Methods */}
      <div className="analysis-methods">
        {/* TextBlob Results */}
        <div className="method-card">
          <h3 className="method-title">
            <span className="method-icon">📊</span>
            TextBlob Analysis
          </h3>
          <div className="method-results">
            <div className="result-item">
              <span className="result-label">Sentiment:</span>
              <span className="result-value" style={{ color: getSentimentColor(textblob.label) }}>
                {textblob.label}
              </span>
            </div>
            <div className="result-item">
              <span className="result-label">Polarity:</span>
              <span className="result-value">{textblob.polarity}</span>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{
                    width: `${(textblob.polarity + 1) * 50}%`,
                    backgroundColor: textblob.polarity > 0 ? '#4caf50' : textblob.polarity < 0 ? '#f44336' : '#ff9800'
                  }}
                />
              </div>
            </div>
            <div className="result-item">
              <span className="result-label">Subjectivity:</span>
              <span className="result-value">{textblob.subjectivity}</span>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${textblob.subjectivity * 100}%`, backgroundColor: '#2196f3' }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* VADER Results */}
        <div className="method-card">
          <h3 className="method-title">
            <span className="method-icon">⚡</span>
            VADER Analysis
          </h3>
          <div className="method-results">
            <div className="result-item">
              <span className="result-label">Sentiment:</span>
              <span className="result-value" style={{ color: getSentimentColor(vader.label) }}>
                {vader.label}
              </span>
            </div>
            <div className="result-item">
              <span className="result-label">Compound Score:</span>
              <span className="result-value">{vader.compound}</span>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{
                    width: `${(vader.compound + 1) * 50}%`,
                    backgroundColor: vader.compound > 0 ? '#4caf50' : vader.compound < 0 ? '#f44336' : '#ff9800'
                  }}
                />
              </div>
            </div>
            <div className="result-item">
              <span className="result-label">Positive:</span>
              <span className="result-value">{formatPercentage(vader.positive)}</span>
            </div>
            <div className="result-item">
              <span className="result-label">Neutral:</span>
              <span className="result-value">{formatPercentage(vader.neutral)}</span>
            </div>
            <div className="result-item">
              <span className="result-label">Negative:</span>
              <span className="result-value">{formatPercentage(vader.negative)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Analyzed Text Preview */}
      <div className="analyzed-text-preview">
        <h3>Analyzed Text</h3>
        <div className="text-preview-content">
          {text}
        </div>
      </div>
    </div>
  );
};

export default SentimentResults;

