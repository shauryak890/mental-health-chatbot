import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import LandingPage from './components/LandingPage';
import Chatbot from './components/Chatbot';
import Resources from './components/Resources';

function App() {
  const [showChat, setShowChat] = useState(false);
  
  // Import fonts
  useEffect(() => {
    // Primary font - Inter
    const interLink = document.createElement('link');
    interLink.rel = 'stylesheet';
    interLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap';
    document.head.appendChild(interLink);
    
    // Secondary display font - Manrope for headings
    const manropeLink = document.createElement('link');
    manropeLink.rel = 'stylesheet';
    manropeLink.href = 'https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap';
    document.head.appendChild(manropeLink);
    
    return () => {
      document.head.removeChild(interLink);
      document.head.removeChild(manropeLink);
    };
  }, []);

  // Handle starting chat from any page
  const handleStartChat = () => {
    setShowChat(true);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={
            !showChat ? 
              <LandingPage onStartChat={handleStartChat} /> : 
              <Navigate to="/chat" replace />
          } />
          <Route path="/resources" element={<Resources />} />
          <Route path="/chat" element={
            <Chatbot onBack={() => {
              setShowChat(false);
              return <Navigate to="/" replace />;
            }} />
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 