/**
 * Result panel component
 * Displays analysis results including understood/misunderstood/missing concepts
 */

import React from 'react';

function ConceptList({ concepts, title, className, emptyMessage }) {
  if (!concepts || concepts.length === 0) {
    return (
      <div className={`concept-section ${className}`}>
        <h3>{title}</h3>
        <div style={{ 
          padding: '1.5rem', 
          textAlign: 'center', 
          color: '#6b7280',
          fontStyle: 'italic',
          background: '#f9fafb',
          borderRadius: '12px',
          border: '2px dashed #d1d5db'
        }}>
          {emptyMessage}
        </div>
      </div>
    );
  }

  return (
    <div className={`concept-section ${className}`}>
      <h3>{title}</h3>
      <ul>
        {concepts.map((concept, index) => (
          <li key={index}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div style={{ flex: 1 }}>
                <strong>{concept.name}</strong>
                <span className="confidence">
                  {(concept.confidence * 100).toFixed(0)}% confidence
                </span>
              </div>
              <div style={{ 
                background: getConfidenceColor(concept.confidence),
                color: 'white',
                padding: '0.25rem 0.5rem',
                borderRadius: '6px',
                fontSize: '0.75rem',
                fontWeight: '600'
              }}>
                {getConfidenceLabel(concept.confidence)}
              </div>
            </div>
            {concept.details && (
              <p className="concept-details">{concept.details}</p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

function getConfidenceColor(confidence) {
  if (confidence >= 0.8) return '#059669';
  if (confidence >= 0.6) return '#d97706';
  return '#dc2626';
}

function getConfidenceLabel(confidence) {
  if (confidence >= 0.8) return 'High';
  if (confidence >= 0.6) return 'Medium';
  return 'Low';
}

function ScoreCircle({ score, label, color }) {
  const circumference = 2 * Math.PI * 45;
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (score * circumference);

  return (
    <div className="score-item" style={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ position: 'relative', width: '100px', height: '100px', marginBottom: '0.5rem' }}>
        <svg width="100" height="100" style={{ transform: 'rotate(-90deg)' }}>
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="#e5e7eb"
            strokeWidth="8"
            fill="transparent"
          />
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke={color}
            strokeWidth="8"
            fill="transparent"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 1s ease-in-out' }}
          />
        </svg>
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          fontSize: '1.25rem',
          fontWeight: '700',
          color: color
        }}>
          {(score * 100).toFixed(0)}%
        </div>
      </div>
      <label style={{ fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
        {label}
      </label>
    </div>
  );
}

function ResultPanel({ result }) {
  if (!result) {
    return null;
  }

  return (
    <div className="result-panel">
      <h2>📊 Analysis Results</h2>
      
      <div className="scores-summary" style={{ display: 'flex', justifyContent: 'space-around', marginBottom: '2rem' }}>
        <ScoreCircle 
          score={result.overall_score} 
          label="Overall Score" 
          color="#667eea"
        />
        <ScoreCircle 
          score={result.coverage_score} 
          label="Coverage" 
          color="#059669"
        />
        <ScoreCircle 
          score={result.correctness_score} 
          label="Correctness" 
          color="#dc2626"
        />
      </div>

      <ConceptList 
        concepts={result.concepts_understood}
        title="✅ Concepts You Understand Well"
        className="understood"
        emptyMessage="No concepts identified as fully understood yet. Keep explaining!"
      />

      <ConceptList 
        concepts={result.concepts_misunderstood}
        title="❌ Concepts That Need Clarification"
        className="misunderstood"
        emptyMessage="Great! No major misunderstandings detected in your explanation."
      />

      <ConceptList 
        concepts={result.concepts_missing}
        title="❓ Important Concepts to Explore"
        className="missing"
        emptyMessage="Excellent coverage! You've touched on all the key concepts."
      />

      {result.feedback && (
        <div className="feedback-section">
          <h3>💡 Personalized Feedback</h3>
          <p style={{ lineHeight: '1.6', fontSize: '1rem' }}>{result.feedback}</p>
        </div>
      )}

      {result.suggestions && result.suggestions.length > 0 && (
        <div className="suggestions-section">
          <h3>🎯 Next Steps for Learning</h3>
          <ul>
            {result.suggestions.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}

      <div style={{ 
        marginTop: '2rem', 
        padding: '1rem', 
        background: 'linear-gradient(135deg, #fef3c7, #fde68a)',
        borderRadius: '12px',
        border: '1px solid #f59e0b',
        textAlign: 'center'
      }}>
        <p style={{ color: '#92400e', fontWeight: '500', margin: 0 }}>
          🚀 <strong>Keep Learning!</strong> Try explaining another concept to continue improving your understanding.
        </p>
      </div>
    </div>
  );
}

export default ResultPanel;