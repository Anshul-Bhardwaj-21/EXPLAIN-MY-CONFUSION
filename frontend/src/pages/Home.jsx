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
  const [hasStarted, setHasStarted] = useState(false);

  const handleAnalyze = async (explanation, topic, subject) => {
    setHasStarted(true);
    setIsLoading(true);
    setAnalysisResult(null);
    
    try {
      const result = await analyzeExplanation(explanation, topic, subject);
      setAnalysisResult(result);
    } catch (err) {
      console.error('Analysis error:', err);
      // Silently handle errors - no user-facing error message
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartNew = () => {
    setAnalysisResult(null);
    setHasStarted(false);
  };

  return (
    <div className="home-container" style={{ 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: analysisResult ? '0' : '2rem 1rem',
      width: '100vw',
      margin: '0',
      boxSizing: 'border-box'
    }}>
      {!hasStarted && !isLoading && !analysisResult && <WelcomeCard />}
      
      {!isLoading && !analysisResult && (
        <div className="card" style={{
          background: 'rgba(255, 255, 255, 0.98)',
          backdropFilter: 'blur(25px)',
          borderRadius: '24px',
          padding: '2.5rem',
          boxShadow: '0 25px 50px rgba(0, 0, 0, 0.15)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          maxWidth: '800px',
          margin: '0 auto',
          transform: 'translateY(0)',
          transition: 'all 0.4s ease'
        }}>
          <TextInput 
            onAnalyze={handleAnalyze} 
            isLoading={isLoading} 
          />
        </div>
      )}
      
      {isLoading && <LoadingSpinner />}
      
      {analysisResult && (
        <div style={{
          width: '100vw',
          minHeight: '100vh',
          margin: '0',
          padding: '0',
          boxSizing: 'border-box',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}>
          <div style={{
            background: 'rgba(255, 255, 255, 0.98)',
            backdropFilter: 'blur(25px)',
            width: '100%',
            minHeight: '100vh',
            margin: '0',
            padding: '3rem',
            boxSizing: 'border-box',
            borderRadius: '0',
            border: 'none',
            animation: 'slideInUp 0.6s ease-out'
          }}>
            <ResultPanel result={analysisResult} />
            
            {/* Try Another Section - Integrated */}
            <div style={{
              marginTop: '3rem',
              padding: '2rem',
              background: 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
              borderRadius: '20px',
              border: '1px solid rgba(102, 126, 234, 0.2)',
              textAlign: 'center'
            }}>
              <h3 style={{ 
                color: '#374151', 
                marginBottom: '1rem',
                fontSize: '1.6rem',
                fontWeight: '700',
                background: 'linear-gradient(135deg, #667eea, #764ba2)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>
                🔄 Try Another Concept
              </h3>
              <p style={{ color: '#6b7280', marginBottom: '2rem', fontSize: '1.1rem', lineHeight: '1.6' }}>
                Ready to test your understanding of another topic?
              </p>
              <button
                onClick={handleStartNew}
                style={{
                  background: 'linear-gradient(135deg, #667eea, #764ba2)',
                  color: 'white',
                  border: 'none',
                  padding: '1.2rem 2.5rem',
                  borderRadius: '18px',
                  fontSize: '1.1rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                  boxShadow: '0 10px 25px rgba(102, 126, 234, 0.3)',
                  position: 'relative',
                  overflow: 'hidden'
                }}
                onMouseOver={(e) => {
                  e.target.style.transform = 'translateY(-3px) scale(1.02)';
                  e.target.style.boxShadow = '0 15px 35px rgba(102, 126, 234, 0.4)';
                }}
                onMouseOut={(e) => {
                  e.target.style.transform = 'translateY(0) scale(1)';
                  e.target.style.boxShadow = '0 10px 25px rgba(102, 126, 234, 0.3)';
                }}
              >
                Start New Analysis
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;