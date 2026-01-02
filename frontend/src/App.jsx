/**
 * Main App component
 * Root component that manages routing and global state
 */

import React from 'react';
import Home from './pages/Home';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            🧠
          </div>
          <div className="header-text">
            <h1>Explain My Confusion</h1>
            <p>AI-powered educational diagnostic tool for computer science concepts</p>
          </div>
        </div>
      </header>
      <main className="app-main">
        <Home />
      </main>
      <footer style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        padding: '1.5rem 2rem',
        textAlign: 'center',
        borderTop: '1px solid rgba(255, 255, 255, 0.2)',
        color: '#6b7280',
        fontSize: '0.875rem'
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <p style={{ margin: 0 }}>
            Built with ❤️ for better learning • Powered by AI & NLP • 
            <span style={{ color: '#667eea', fontWeight: '600' }}> Keep Learning, Keep Growing!</span>
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;