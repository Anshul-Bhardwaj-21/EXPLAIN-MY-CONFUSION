/**
 * Home page component
 * Main interface for text input and results display
 */

import React, { useState } from 'react';
import TextInput from '../components/TextInput';
import ResultPanel from '../components/ResultPanel';
import LoadingSpinner from '../components/LoadingSpinner';
import WelcomeCard from '../components/WelcomeCard';
import { analyzeExplanation } from '../services/api';

function Home() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasStarted, setHasStarted] = useState(false);

  const handleAnalyze = async (explanation, subject, topic) => {
    setHasStarted(true);
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);
    
    try {
      const result = await analyzeExplanation(explanation, subject, topic);
      setAnalysisResult(result);
    } catch (err) {
      setError('Failed to analyze explanation. Please check your connection and try again.');
      console.error('Analysis error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartNew = () => {
    setAnalysisResult(null);
    setError(null);
    setHasStarted(false);
  };

  return (
    <div className="home-container">
      {!hasStarted && !isLoading && !analysisResult && <WelcomeCard />}
      
      {!isLoading && !analysisResult && (
        <div className="card">
          <TextInput 
            onAnalyze={handleAnalyze} 
            isLoading={isLoading} 
          />
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
        </div>
      )}
      
      {isLoading && <LoadingSpinner />}
      
      {analysisResult && (
        <>
          <div className="card">
            <ResultPanel result={analysisResult} />
          </div>
          <div className="card">
            <div style={{ textAlign: 'center' }}>
              <h3 style={{ 
                color: '#374151', 
                marginBottom: '1rem',
                fontSize: '1.25rem',
                fontWeight: '600'
              }}>
                🔄 Try Another Concept
              </h3>
              <p style={{ color: '#6b7280', marginBottom: '1.5rem' }}>
                Ready to test your understanding of another topic?
              </p>
              <button
                onClick={handleStartNew}
                style={{
                  background: 'linear-gradient(135deg, #667eea, #764ba2)',
                  color: 'white',
                  border: 'none',
                  padding: '0.75rem 1.5rem',
                  borderRadius: '12px',
                  fontSize: '1rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
                onMouseOver={(e) => {
                  e.target.style.transform = 'translateY(-1px)';
                  e.target.style.boxShadow = '0 8px 25px rgba(102, 126, 234, 0.3)';
                }}
                onMouseOut={(e) => {
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = 'none';
                }}
              >
                Start New Analysis
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default Home;