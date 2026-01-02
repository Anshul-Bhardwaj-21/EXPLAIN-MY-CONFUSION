/**
 * Welcome card component
 * Displays helpful information for new users
 */

import React from 'react';

function WelcomeCard() {
  return (
    <div className="card" style={{ 
      background: 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
      border: '1px solid #bae6fd',
      marginBottom: '2rem'
    }}>
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>🎓</div>
        <h2 style={{ 
          color: '#0369a1', 
          fontSize: '1.5rem', 
          fontWeight: '700',
          marginBottom: '0.5rem'
        }}>
          Welcome to Explain My Confusion!
        </h2>
        <p style={{ color: '#0284c7', fontSize: '1rem' }}>
          Test and improve your understanding of computer science concepts
        </p>
      </div>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
        gap: '1rem',
        marginBottom: '1.5rem'
      }}>
        <div style={{ 
          background: 'white', 
          padding: '1rem', 
          borderRadius: '12px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📝</div>
          <h4 style={{ color: '#374151', marginBottom: '0.5rem' }}>1. Choose & Explain</h4>
          <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
            Select a CS topic and explain it in your own words
          </p>
        </div>
        
        <div style={{ 
          background: 'white', 
          padding: '1rem', 
          borderRadius: '12px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🧠</div>
          <h4 style={{ color: '#374151', marginBottom: '0.5rem' }}>2. AI Analysis</h4>
          <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
            Our AI analyzes your understanding and identifies gaps
          </p>
        </div>
        
        <div style={{ 
          background: 'white', 
          padding: '1rem', 
          borderRadius: '12px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🎯</div>
          <h4 style={{ color: '#374151', marginBottom: '0.5rem' }}>3. Get Feedback</h4>
          <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
            Receive personalized feedback and learning suggestions
          </p>
        </div>
      </div>
      
      <div style={{ 
        background: 'rgba(255, 255, 255, 0.7)',
        padding: '1rem',
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <p style={{ 
          color: '#0369a1', 
          fontSize: '0.875rem', 
          margin: 0,
          fontWeight: '500'
        }}>
          💡 <strong>Pro Tip:</strong> The more detailed your explanation, the better feedback you'll receive!
        </p>
      </div>
    </div>
  );
}

export default WelcomeCard;