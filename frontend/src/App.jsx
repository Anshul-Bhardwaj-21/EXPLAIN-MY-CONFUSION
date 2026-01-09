/**
 * Main App component
 * Root component that manages routing and global state
 */

import React from 'react';
import Home from './pages/Home';
import './App.css';

function App() {
  return (
    <div className="App" style={{ margin: 0, padding: 0, width: '100vw', overflow: 'hidden' }}>
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
      <main className="app-main" style={{ margin: 0, padding: 0, width: '100vw' }}>
        <Home />
      </main>
    </div>
  );
}

export default App;