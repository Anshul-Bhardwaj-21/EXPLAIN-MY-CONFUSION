/**
 * Result panel component for real NLP analysis results
 * Displays Wikipedia-based concept comparison and feedback
 */

import React from 'react';

function ConceptSection({ title, concepts, color, emptyMessage }) {
  if (!concepts || concepts.length === 0) {
    return (
      <div className="concept-section" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: color, marginBottom: '0.5rem' }}>{title}</h3>
        <div style={{ 
          padding: '1rem', 
          background: '#f9fafb',
          borderRadius: '8px',
          color: '#6b7280',
          fontStyle: 'italic',
          border: '2px dashed #d1d5db'
        }}>
          {emptyMessage}
        </div>
      </div>
    );
  }

  return (
    <div className="concept-section" style={{ marginBottom: '1.5rem' }}>
      <h3 style={{ color: color, marginBottom: '0.5rem' }}>{title}</h3>
      <div style={{ 
        background: 'white',
        borderRadius: '8px',
        border: `2px solid ${color}20`,
        padding: '1rem'
      }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
          {concepts.map((concept, index) => (
            <span 
              key={index}
              style={{
                background: `${color}15`,
                color: color,
                padding: '0.25rem 0.75rem',
                borderRadius: '20px',
                fontSize: '0.875rem',
                fontWeight: '500',
                border: `1px solid ${color}30`
              }}
            >
              {concept}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

function ResultPanel({ result }) {
  if (!result) {
    return null;
  }

  if (!result.success) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
        <h2 style={{ color: '#dc2626', marginBottom: '1rem' }}>❌ Analysis Failed</h2>
        <p style={{ color: '#6b7280', marginBottom: '1rem' }}>
          {result.error || 'Unable to analyze your explanation'}
        </p>
        <div style={{ 
          background: '#fef3c7', 
          padding: '1rem', 
          borderRadius: '8px',
          color: '#92400e'
        }}>
          <strong>Tip:</strong> Try using a more specific or well-known topic. 
          The system works best with topics that have Wikipedia articles.
        </div>
      </div>
    );
  }

  const { student_analysis, reference_info, concept_analysis, explanations, learning_suggestions } = result;

  return (
    <div className="result-panel">
      <h2 style={{ marginBottom: '1.5rem', color: '#1f2937' }}>
        📊 Analysis Results for "{result.topic}"
      </h2>

      {/* Reference Information */}
      <div style={{ 
        background: '#f0f9ff', 
        padding: '1rem', 
        borderRadius: '8px', 
        marginBottom: '1.5rem',
        border: '1px solid #bae6fd'
      }}>
        <h3 style={{ color: '#0369a1', marginBottom: '0.5rem' }}>📚 Reference Source</h3>
        <p style={{ margin: '0.5rem 0', color: '#374151' }}>
          <strong>Wikipedia Article:</strong> {reference_info.title}
        </p>
        <p style={{ margin: '0.5rem 0', color: '#6b7280', fontSize: '0.9rem' }}>
          {reference_info.summary_preview}
        </p>
        <a 
          href={reference_info.url} 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ color: '#2563eb', textDecoration: 'none', fontSize: '0.875rem' }}
        >
          🔗 View full Wikipedia article
        </a>
      </div>

      {/* Student Analysis Summary */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', 
        gap: '1rem',
        marginBottom: '1.5rem'
      }}>
        <div className="score-item">
          <label>Words</label>
          <span>{student_analysis.word_count}</span>
        </div>
        <div className="score-item">
          <label>Sentences</label>
          <span>{student_analysis.sentence_count}</span>
        </div>
        <div className="score-item">
          <label>Similarity</label>
          <span>{(concept_analysis.similarity_score * 100).toFixed(0)}%</span>
        </div>
        <div className="score-item">
          <label>Key Terms</label>
          <span>{student_analysis.key_terms.length}</span>
        </div>
      </div>

      {/* Concept Analysis */}
      <ConceptSection
        title="✅ Concepts You Got Right"
        concepts={concept_analysis.correct_concepts}
        color="#059669"
        emptyMessage="No matching concepts found with the reference material"
      />

      <ConceptSection
        title="❓ Important Concepts You Missed"
        concepts={concept_analysis.missing_concepts}
        color="#d97706"
        emptyMessage="Great! You covered all the main concepts from the reference"
      />

      <ConceptSection
        title="🤔 Extra Concepts You Mentioned"
        concepts={concept_analysis.extra_concepts}
        color="#7c3aed"
        emptyMessage="You stayed focused on the core concepts"
      />

      {/* Detailed Explanations */}
      <div style={{ marginTop: '2rem' }}>
        <div className="feedback-section">
          <h3>✅ What You Got Right</h3>
          <p>{explanations.what_you_got_right}</p>
        </div>

        <div className="feedback-section">
          <h3>❓ What You Missed</h3>
          <p>{explanations.what_you_missed}</p>
        </div>

        <div className="feedback-section">
          <h3>🤔 Where Confusion Might Be</h3>
          <p>{explanations.where_confusion_is}</p>
        </div>
      </div>

      {/* Learning Suggestions */}
      {learning_suggestions && learning_suggestions.length > 0 && (
        <div className="suggestions-section">
          <h3>🎯 Learning Suggestions</h3>
          <ul>
            {learning_suggestions.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Footer */}
      <div style={{ 
        marginTop: '2rem', 
        padding: '1rem', 
        background: 'linear-gradient(135deg, #fef3c7, #fde68a)',
        borderRadius: '12px',
        border: '1px solid #f59e0b',
        textAlign: 'center'
      }}>
        <p style={{ color: '#92400e', fontWeight: '500', margin: 0 }}>
          🧠 <strong>Powered by Real Knowledge:</strong> This analysis used actual Wikipedia content 
          and natural language processing to compare your explanation with expert knowledge.
        </p>
      </div>
    </div>
  );
}

export default ResultPanel;