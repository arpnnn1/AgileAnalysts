import React from 'react';
import './CandidateEvaluation.css';

const CandidateEvaluation = ({ evaluation, transcription, facialExpressionAnalysis }) => {
  // Prioritize facial expression analysis over text-based evaluation
  const analysis = facialExpressionAnalysis || evaluation;
  
  // Check for errors
  const hasError = analysis?.error || evaluation?.transcription_error || evaluation?.evaluation_error;
  const errorMessage = analysis?.error || evaluation?.transcription_error || evaluation?.evaluation_error;
  
  if (!analysis && !transcription) {
    return null; // Don't show anything if no data
  }
  
  // If analysis has errors but no scores, show error
  if (!analysis?.scores && hasError && !transcription?.text) {
    return (
      <div className="candidate-evaluation-container">
        <div className="error-message">
          <strong>Facial Expression Analysis Unavailable</strong>
          <p>{errorMessage}</p>
          <p style={{ marginTop: '10px', fontSize: '0.9rem' }}>
            Facial expression analysis requires PyTorch and torchvision.
            <br />
            Install: <code>pip install torch torchvision Pillow</code>
          </p>
        </div>
      </div>
    );
  }

  // If we have transcription but no analysis, show transcription only
  if (transcription?.text && !analysis?.scores) {
    return (
      <div className="candidate-evaluation-container">
        <div className="transcription-section">
          <h3>Interview Transcription</h3>
          <div className="transcription-text">
            {transcription.text}
          </div>
          <div className="transcription-meta">
            <span>Language: {transcription.language || 'Auto-detected'}</span>
            <span>Words: {transcription.text.split(' ').length}</span>
          </div>
        </div>
        {hasError && (
          <div className="error-message" style={{ marginTop: '20px' }}>
            <strong>Facial Expression Analysis Unavailable</strong>
            <p>{errorMessage}</p>
          </div>
        )}
      </div>
    );
  }

  const { scores, overall_score } = analysis || {};
  const overall_sentiment = evaluation?.overall_sentiment; // Only from text evaluation
  
  // If no scores available and no transcription, don't render anything
  if (!scores && !transcription?.text) {
    return null;
  }
  
  // Determine analysis source
  const analysisSource = facialExpressionAnalysis ? 'Facial Expression Analysis' : 'Text-Based Analysis';
  
  const parameterNames = {
    confidence: "Confidence",
    authenticity: "Authenticity",
    leadership: "Leadership",
    pressure_handling: "Pressure Handling"
  };

  const getScoreColor = (score) => {
    if (score >= 0.7) return '#4caf50'; // Green
    if (score >= 0.5) return '#ff9800'; // Orange
    return '#f44336'; // Red
  };

  const getScoreLabel = (score) => {
    if (score >= 0.8) return 'Excellent';
    if (score >= 0.7) return 'Good';
    if (score >= 0.5) return 'Average';
    if (score >= 0.3) return 'Below Average';
    return 'Poor';
  };

  const formatPercentage = (score) => {
    return `${(score * 100).toFixed(0)}%`;
  };

  return (
    <div className="candidate-evaluation-container">
      <div className="evaluation-header">
        <div>
          <h2>Candidate Evaluation</h2>
          <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '5px' }}>
            Based on {analysisSource}
          </p>
        </div>
        {overall_score !== undefined && (
          <div className="overall-score-badge" style={{ backgroundColor: getScoreColor(overall_score) }}>
            <span className="overall-score-value">{formatPercentage(overall_score)}</span>
            <span className="overall-score-label">Overall Score</span>
          </div>
        )}
      </div>
      
      {facialExpressionAnalysis && (
        <div className="analysis-info" style={{ 
          background: '#f0f0ff', 
          padding: '10px 15px', 
          borderRadius: '6px', 
          marginBottom: '20px',
          fontSize: '0.9rem',
          color: '#555'
        }}>
          <strong>Frames Analyzed:</strong> {facialExpressionAnalysis.frame_count || 0} / {facialExpressionAnalysis.frames_analyzed || 0}
        </div>
      )}

      {transcription && transcription.text && (
        <div className="transcription-section">
          <h3>Interview Transcription</h3>
          <div className="transcription-text">
            {transcription.text}
          </div>
          <div className="transcription-meta">
            <span>Language: {transcription.language || 'Auto-detected'}</span>
            <span>Words: {evaluation.word_count || transcription.text.split(' ').length}</span>
          </div>
        </div>
      )}

      {overall_sentiment && (
        <div className="sentiment-summary">
          <h3>Overall Sentiment</h3>
          <div className="sentiment-badge" style={{ 
            backgroundColor: overall_sentiment.label === 'positive' ? '#4caf50' : 
                           overall_sentiment.label === 'negative' ? '#f44336' : '#ff9800'
          }}>
            <span className="sentiment-label">{overall_sentiment.label.toUpperCase()}</span>
            <span className="sentiment-confidence">
              Confidence: {formatPercentage(overall_sentiment.confidence || 0)}
            </span>
          </div>
        </div>
      )}

      <div className="scores-section">
        <h3>Evaluation Parameters</h3>
        <div className="scores-grid">
          {Object.entries(scores || {}).map(([key, score]) => (
            <div key={key} className="score-card">
              <div className="score-header">
                <h4>{parameterNames[key] || key}</h4>
                <span className="score-value" style={{ color: getScoreColor(score) }}>
                  {formatPercentage(score)}
                </span>
              </div>
              <div className="score-bar-container">
                <div 
                  className="score-bar-fill" 
                  style={{ 
                    width: `${score * 100}%`,
                    backgroundColor: getScoreColor(score)
                  }}
                />
              </div>
              <div className="score-label">{getScoreLabel(score)}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="evaluation-summary">
        <h3>Summary</h3>
        <div className="summary-content">
          <p>
            The candidate demonstrates <strong>{getScoreLabel(overall_score)}</strong> overall performance 
            with an overall score of <strong>{formatPercentage(overall_score)}</strong>.
          </p>
          {scores && (
            <ul className="summary-points">
              {Object.entries(scores)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 3)
                .map(([key, score]) => (
                  <li key={key}>
                    <strong>{parameterNames[key] || key}</strong>: {getScoreLabel(score)} ({formatPercentage(score)})
                  </li>
                ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default CandidateEvaluation;

