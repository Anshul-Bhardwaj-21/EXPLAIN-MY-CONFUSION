/**
 * Loading spinner component
 * Displays an animated loading state during analysis
 */

import React from 'react';

function LoadingSpinner() {
  return (
    <div className="card" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <div style={{
          width: '60px',
          height: '60px',
          border: '4px solid #e5e7eb',
          borderTop: '4px solid #667eea',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
          margin: '0 auto'
        }}></div>
      </div>
      
      <h3 style={{ 
        color: '#374151', 
        marginBottom: '0.5rem',
        fontSize: '1.25rem',
        fontWeight: '600'
      }}>
        🧠 Analyzing Your Understanding...
      </h3>
      
      <p style={{ color: '#6b7280', fontSize: '1rem', lineHeight: '1.5' }}>
        Our AI is carefully examining your explanation and comparing it with expert knowledge.
        This may take a few moments.
      </p>
      
      <div style={{ 
        marginTop: '1.5rem',
        display: 'flex',
        justifyContent: 'center',
        gap: '0.5rem'
      }}>
        <div style={{
          width: '8px',
          height: '8px',
          backgroundColor: '#667eea',
          borderRadius: '50%',
          animation: 'bounce 1.4s ease-in-out infinite both',
          animationDelay: '0s'
        }}></div>
        <div style={{
          width: '8px',
          height: '8px',
          backgroundColor: '#667eea',
          borderRadius: '50%',
          animation: 'bounce 1.4s ease-in-out infinite both',
          animationDelay: '0.16s'
        }}></div>
        <div style={{
          width: '8px',
          height: '8px',
          backgroundColor: '#667eea',
          borderRadius: '50%',
          animation: 'bounce 1.4s ease-in-out infinite both',
          animationDelay: '0.32s'
        }}></div>
      </div>
      
      <style jsx>{`
        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
          }
          40% {
            transform: scale(1);
          }
        }
      `}</style>
    </div>
  );
}

export default LoadingSpinner;