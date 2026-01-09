/**
 * Result panel component for real NLP analysis results
 * Displays Wikipedia-based concept comparison and feedback
 */

import React from 'react';

function ConceptSection({ title, concepts, color, emptyMessage }) {
  if (!concepts || concepts.length === 0) {
    return (
      <div className="concept-section" style={{ marginBottom: '2rem' }}>
        <h3 style={{ 
          color: color, 
          marginBottom: '1rem',
          fontSize: '1.3rem',
          fontWeight: '700',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          {title}
        </h3>
        <div style={{ 
          padding: '2rem', 
          background: 'linear-gradient(135deg, #f9fafb, #f3f4f6)',
          borderRadius: '16px',
          color: '#6b7280',
          fontStyle: 'italic',
          border: '2px dashed #d1d5db',
          textAlign: 'center',
          fontSize: '1.1rem'
        }}>
          {emptyMessage}
        </div>
      </div>
    );
  }

  return (
    <div className="concept-section" style={{ marginBottom: '2rem' }}>
      <h3 style={{ 
        color: color, 
        marginBottom: '1rem',
        fontSize: '1.3rem',
        fontWeight: '700',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
      }}>
        {title}
      </h3>
      <div style={{ 
        background: 'white',
        borderRadius: '16px',
        border: `3px solid ${color}20`,
        padding: '1.5rem',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)'
      }}>
        <div style={{ 
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
          gap: '1rem'
        }}>
          {concepts.map((concept, index) => (
            <div
              key={index}
              style={{
                background: `linear-gradient(135deg, ${color}10, ${color}05)`,
                color: color,
                padding: '1rem 1.5rem',
                borderRadius: '12px',
                fontSize: '1rem',
                fontWeight: '600',
                border: `2px solid ${color}30`,
                textAlign: 'center',
                transition: 'all 0.3s ease',
                cursor: 'default',
                position: 'relative',
                overflow: 'hidden'
              }}
              onMouseOver={(e) => {
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = `0 8px 20px ${color}20`;
              }}
              onMouseOut={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = 'none';
              }}
            >
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '3px',
                background: color
              }}></div>
              {concept}
            </div>
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
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
        gap: '1.5rem',
        marginBottom: '2rem'
      }}>
        <div className="score-item" style={{
          background: 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
          padding: '1.5rem',
          borderRadius: '16px',
          textAlign: 'center',
          border: '2px solid #bae6fd',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '4px',
            background: 'linear-gradient(90deg, #0ea5e9, #06b6d4)'
          }}></div>
          <label style={{ fontSize: '0.9rem', color: '#0369a1', fontWeight: '600' }}>Words</label>
          <span style={{ fontSize: '2rem', fontWeight: '800', color: '#0c4a6e', display: 'block' }}>
            {student_analysis.word_count}
          </span>
        </div>
        
        <div className="score-item" style={{
          background: 'linear-gradient(135deg, #f0fdf4, #dcfce7)',
          padding: '1.5rem',
          borderRadius: '16px',
          textAlign: 'center',
          border: '2px solid #bbf7d0',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '4px',
            background: 'linear-gradient(90deg, #10b981, #059669)'
          }}></div>
          <label style={{ fontSize: '0.9rem', color: '#059669', fontWeight: '600' }}>Sentences</label>
          <span style={{ fontSize: '2rem', fontWeight: '800', color: '#064e3b', display: 'block' }}>
            {student_analysis.sentence_count}
          </span>
        </div>
        
        <div className="score-item" style={{
          background: 'linear-gradient(135deg, #fefce8, #fef3c7)',
          padding: '1.5rem',
          borderRadius: '16px',
          textAlign: 'center',
          border: '2px solid #fde68a',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '4px',
            background: 'linear-gradient(90deg, #f59e0b, #d97706)'
          }}></div>
          <label style={{ fontSize: '0.9rem', color: '#d97706', fontWeight: '600' }}>Similarity</label>
          <span style={{ fontSize: '2rem', fontWeight: '800', color: '#92400e', display: 'block' }}>
            {(concept_analysis.similarity_score * 100).toFixed(0)}%
          </span>
          <div style={{
            marginTop: '0.5rem',
            height: '6px',
            background: '#fde68a',
            borderRadius: '3px',
            overflow: 'hidden'
          }}>
            <div style={{
              height: '100%',
              width: `${concept_analysis.similarity_score * 100}%`,
              background: 'linear-gradient(90deg, #f59e0b, #d97706)',
              borderRadius: '3px',
              transition: 'width 1s ease-out'
            }}></div>
          </div>
        </div>
        
        <div className="score-item" style={{
          background: 'linear-gradient(135deg, #fdf2f8, #fce7f3)',
          padding: '1.5rem',
          borderRadius: '16px',
          textAlign: 'center',
          border: '2px solid #f9a8d4',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '4px',
            background: 'linear-gradient(90deg, #ec4899, #db2777)'
          }}></div>
          <label style={{ fontSize: '0.9rem', color: '#be185d', fontWeight: '600' }}>Key Terms</label>
          <span style={{ fontSize: '2rem', fontWeight: '800', color: '#831843', display: 'block' }}>
            {student_analysis.key_terms.length}
          </span>
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
      <div style={{ 
        marginTop: '3rem',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '2rem'
      }}>
        <div style={{
          background: 'linear-gradient(135deg, #f0fdf4, #dcfce7)',
          padding: '2rem',
          borderRadius: '20px',
          border: '3px solid #bbf7d0',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '5px',
            background: 'linear-gradient(90deg, #10b981, #059669)'
          }}></div>
          <h3 style={{
            color: '#059669',
            fontSize: '1.4rem',
            fontWeight: '700',
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            ✅ What You Got Right
          </h3>
          <p style={{
            color: '#064e3b',
            fontSize: '1.1rem',
            lineHeight: '1.6',
            margin: 0
          }}>
            {explanations.what_you_got_right}
          </p>
        </div>

        <div style={{
          background: 'linear-gradient(135deg, #fefce8, #fef3c7)',
          padding: '2rem',
          borderRadius: '20px',
          border: '3px solid #fde68a',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '5px',
            background: 'linear-gradient(90deg, #f59e0b, #d97706)'
          }}></div>
          <h3 style={{
            color: '#d97706',
            fontSize: '1.4rem',
            fontWeight: '700',
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            ❓ What You Missed
          </h3>
          <p style={{
            color: '#92400e',
            fontSize: '1.1rem',
            lineHeight: '1.6',
            margin: 0
          }}>
            {explanations.what_you_missed}
          </p>
        </div>

        <div style={{
          background: 'linear-gradient(135deg, #fdf2f8, #fce7f3)',
          padding: '2rem',
          borderRadius: '20px',
          border: '3px solid #f9a8d4',
          position: 'relative',
          overflow: 'hidden',
          gridColumn: 'span 2'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '5px',
            background: 'linear-gradient(90deg, #ec4899, #db2777)'
          }}></div>
          <h3 style={{
            color: '#be185d',
            fontSize: '1.4rem',
            fontWeight: '700',
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            🤔 Where Confusion Might Be
          </h3>
          <p style={{
            color: '#831843',
            fontSize: '1.1rem',
            lineHeight: '1.6',
            margin: 0
          }}>
            {explanations.where_confusion_is}
          </p>
        </div>
      </div>

      {/* Learning Suggestions */}
      {learning_suggestions && learning_suggestions.length > 0 && (
        <div style={{
          marginTop: '3rem',
          background: 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
          padding: '2.5rem',
          borderRadius: '24px',
          border: '3px solid #bae6fd',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '6px',
            background: 'linear-gradient(90deg, #0ea5e9, #06b6d4)'
          }}></div>
          <h3 style={{
            color: '#0369a1',
            fontSize: '1.5rem',
            fontWeight: '700',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            🎯 Learning Suggestions
          </h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '1.5rem'
          }}>
            {learning_suggestions.map((suggestion, index) => (
              <div
                key={index}
                style={{
                  background: 'white',
                  padding: '1.5rem',
                  borderRadius: '16px',
                  border: '2px solid #bae6fd',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)',
                  position: 'relative',
                  overflow: 'hidden'
                }}
              >
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  height: '3px',
                  background: '#0ea5e9'
                }}></div>
                <div style={{
                  color: '#0369a1',
                  fontSize: '1.1rem',
                  lineHeight: '1.6',
                  fontWeight: '500'
                }}>
                  {suggestion}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div style={{ 
        marginTop: '3rem', 
        padding: '2rem', 
        background: 'linear-gradient(135deg, #fef3c7, #fde68a)',
        borderRadius: '20px',
        border: '3px solid #f59e0b',
        textAlign: 'center',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '5px',
          background: 'linear-gradient(90deg, #f59e0b, #d97706)'
        }}></div>
        <p style={{ 
          color: '#92400e', 
          fontWeight: '600', 
          margin: 0,
          fontSize: '1.1rem',
          lineHeight: '1.6'
        }}>
          🧠 <strong>Powered by Real Knowledge:</strong> This analysis used actual Wikipedia content 
          and natural language processing to compare your explanation with expert knowledge.
        </p>
        <div style={{
          marginTop: '1rem',
          display: 'flex',
          justifyContent: 'center',
          gap: '2rem',
          flexWrap: 'wrap'
        }}>
          <span style={{ color: '#92400e', fontSize: '0.9rem', fontWeight: '500' }}>
            📚 Wikipedia API
          </span>
          <span style={{ color: '#92400e', fontSize: '0.9rem', fontWeight: '500' }}>
            🤖 NLP Processing
          </span>
          <span style={{ color: '#92400e', fontSize: '0.9rem', fontWeight: '500' }}>
            🧮 Semantic Analysis
          </span>
        </div>
      </div>
    </div>
  );
}

export default ResultPanel;