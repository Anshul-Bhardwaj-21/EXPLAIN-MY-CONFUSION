/**
 * Text input component
 * Handles user input for explanation text, subject, and topic selection
 */

import React, { useState } from 'react';

const SUBJECTS = [
  { value: 'data_structures', label: 'Data Structures', icon: '🏗️' },
  { value: 'algorithms', label: 'Algorithms', icon: '⚡' },
  { value: 'operating_systems', label: 'Operating Systems', icon: '💻' },
  { value: 'databases', label: 'Databases', icon: '🗄️' },
  { value: 'computer_networks', label: 'Computer Networks', icon: '🌐' },
  { value: 'software_engineering', label: 'Software Engineering', icon: '🛠️' }
];

function TextInput({ onAnalyze, isLoading }) {
  const [explanation, setExplanation] = useState('');
  const [subject, setSubject] = useState('');
  const [topic, setTopic] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!explanation.trim() || !subject || !topic.trim()) {
      alert('Please fill in all fields to get the best analysis results.');
      return;
    }
    
    onAnalyze(explanation, subject, topic);
  };

  const selectedSubject = SUBJECTS.find(s => s.value === subject);

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
          📝 Share Your Understanding
        </h2>
        <p style={{ color: '#6b7280', fontSize: '1rem' }}>
          Explain a computer science concept in your own words, and get personalized feedback on your understanding.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="text-input-form">
        <div className="form-group">
          <label htmlFor="subject">
            {selectedSubject ? `${selectedSubject.icon} ` : '📚 '}
            Subject Area
          </label>
          <select 
            id="subject"
            value={subject} 
            onChange={(e) => setSubject(e.target.value)}
            required
          >
            <option value="">Choose your subject...</option>
            {SUBJECTS.map(subj => (
              <option key={subj.value} value={subj.value}>
                {subj.icon} {subj.label}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="topic">
            🎯 Specific Topic
          </label>
          <input
            type="text"
            id="topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., Binary Search Trees, Dijkstra's Algorithm, TCP/IP..."
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="explanation">
            💭 Your Explanation
          </label>
          <textarea
            id="explanation"
            value={explanation}
            onChange={(e) => setExplanation(e.target.value)}
            placeholder="Explain the concept in your own words. Include how it works, when to use it, examples, or any relationships to other concepts you know..."
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
            <span>💡 Tip: The more detailed your explanation, the better feedback you'll receive</span>
            <span>{explanation.length} characters</span>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={isLoading}
          className="analyze-button"
        >
          {isLoading && <span className="loading-spinner"></span>}
          {isLoading ? 'Analyzing Your Understanding...' : '🔍 Analyze My Explanation'}
        </button>
      </form>
    </div>
  );
}

export default TextInput;