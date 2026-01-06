/**
 * Text input component for real NLP analysis
 * Handles user input for topic and explanation
 */

import React, { useState } from 'react';

function TextInput({ onAnalyze, isLoading }) {
  const [explanation, setExplanation] = useState('');
  const [topic, setTopic] = useState('');
  const [subject, setSubject] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!explanation.trim() || !topic.trim()) {
      alert('Please provide both a topic and your explanation.');
      return;
    }
    
    if (explanation.length < 10) {
      alert('Please provide a more detailed explanation (at least 10 characters).');
      return;
    }
    
    onAnalyze(explanation, topic, subject || null);
  };

  return (
    <div>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ 
          fontSize: '1.5rem', 
          fontWeight: '700', 
          color: '#1f2937',
          marginBottom: '0.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          🧠 Explain Your Understanding
        </h2>
        <p style={{ color: '#6b7280', fontSize: '1rem' }}>
          Choose any topic and explain it in your own words. Our system will compare your explanation 
          with Wikipedia knowledge and provide detailed feedback.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="text-input-form">
        <div className="form-group">
          <label htmlFor="topic">
            🎯 Topic (Required)
          </label>
          <input
            type="text"
            id="topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., Binary Search Tree, Machine Learning, Photosynthesis, Democracy..."
            required
          />
          <small style={{ color: '#6b7280', fontSize: '0.875rem' }}>
            Enter any topic you want to explain. The system will find relevant Wikipedia content.
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="subject">
            📚 Subject Area (Optional)
          </label>
          <input
            type="text"
            id="subject"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            placeholder="e.g., Computer Science, Biology, History, Physics..."
          />
          <small style={{ color: '#6b7280', fontSize: '0.875rem' }}>
            Optional: Helps find more specific reference content
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="explanation">
            💭 Your Explanation (Required)
          </label>
          <textarea
            id="explanation"
            value={explanation}
            onChange={(e) => setExplanation(e.target.value)}
            placeholder="Explain the topic in your own words. Include what you think it is, how it works, why it's important, examples, or any other details you know..."
            rows={6}
            required
          />
          <div style={{ 
            fontSize: '0.875rem', 
            color: '#6b7280', 
            marginTop: '0.5rem',
            display: 'flex',
            justifyContent: 'space-between'
          }}>
            <span>💡 Tip: More detailed explanations get better analysis</span>
            <span>{explanation.length} characters</span>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={isLoading}
          className="analyze-button"
        >
          {isLoading && <span className="loading-spinner"></span>}
          {isLoading ? 'Analyzing with Wikipedia Knowledge...' : '🔍 Analyze My Explanation'}
        </button>
        
        {!isLoading && (
          <div style={{ 
            marginTop: '1rem', 
            padding: '1rem', 
            background: '#f0f9ff', 
            borderRadius: '8px',
            fontSize: '0.875rem',
            color: '#0369a1'
          }}>
            <strong>How it works:</strong> Your explanation will be compared with real Wikipedia content 
            using natural language processing to identify what you understand correctly, what you missed, 
            and where there might be confusion.
          </div>
        )}
      </form>
    </div>
  );
}

export default TextInput;