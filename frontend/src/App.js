import React, { useState } from 'react';
import './App.css';
import LandingPage from './components/LandingPage';
import Chatbot from './components/Chatbot';

function App() {
  const [showChat, setShowChat] = useState(false);

  return (
    <div className="App">
      {!showChat ? (
        <LandingPage onStartChat={() => setShowChat(true)} />
      ) : (
        <Chatbot onBack={() => setShowChat(false)} />
      )}
    </div>
  );
}

export default App; 