import React, { useState } from 'react';

function Chatbot({ onBack }) {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = {
      text: inputMessage,
      sender: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setInputMessage('');

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputMessage }),
      });

      const data = await response.json();
      
      const botMessage = {
        text: data.response,
        sender: 'bot'
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <button className="back-button" onClick={onBack}>←</button>
        <h1>University Mental Health Support Chat</h1>
        <p>Feel free to share your concerns. I'm here to help.</p>
      </div>
      
      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <div className="message-content">{message.text}</div>
          </div>
        ))}
        {isLoading && <div className="message bot">
          <div className="message-content">Typing...</div>
        </div>}
      </div>

      <form onSubmit={sendMessage} className="input-form">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message here..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default Chatbot; 