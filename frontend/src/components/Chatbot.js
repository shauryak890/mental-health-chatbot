import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faArrowLeft, 
  faRobot, 
  faPaperPlane,
  faSmile,
  faPaperclip,
  faEllipsisV,
  faShieldAlt,
  faInfoCircle,
  faCog,
  faExternalLinkAlt
} from '@fortawesome/free-solid-svg-icons';

function Chatbot({ onBack }) {
  // State Management
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  // Auto Scroll
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Message Handlers
  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = {
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setInputMessage('');
    setShowEmojiPicker(false);

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
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      // Add error message to chat
      setMessages(prev => [...prev, {
        text: "Sorry, I'm having trouble connecting. Please try again.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Feature Handlers
  const handleEmojiClick = (emoji) => {
    setInputMessage(prev => prev + emoji);
    setShowEmojiPicker(false);
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Add file message to chat
      setMessages(prev => [...prev, {
        text: `Attached file: ${file.name}`,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isFile: true
      }]);
    }
  };

  const menuOptions = [
    { icon: faInfoCircle, label: 'About', action: () => window.open('/about', '_blank') },
    { icon: faCog, label: 'Settings', action: () => window.open('/settings', '_blank') },
    { icon: faExternalLinkAlt, label: 'Resources', action: () => window.open('/resources', '_blank') }
  ];

  // Simple emoji picker
  const emojis = ['😊', '😔', '😢', '😡', '😌', '🤔', '❤️', '👍'];

  return (
    <div className="chat-container">
      {/* Header Section */}
      <div className="chat-header">
        <button className="back-button" onClick={onBack}>
          <FontAwesomeIcon icon={faArrowLeft} />
        </button>
        
        <div className="header-content">
          <div className="header-top">
            <h1>Mental Health Support</h1>
            <div className="header-actions">
              <button 
                className="menu-button"
                onClick={() => setShowMenu(!showMenu)}
              >
                <FontAwesomeIcon icon={faEllipsisV} />
              </button>
              
              {showMenu && (
                <div className="menu-dropdown">
                  {menuOptions.map((option, index) => (
                    <button 
                      key={index} 
                      onClick={option.action}
                      className="menu-option"
                    >
                      <FontAwesomeIcon icon={option.icon} />
                      <span>{option.label}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
          
          <div className="status-indicator">
            <span className="status-dot"></span>
            <span>Online - Ready to Help</span>
            <div className="security-badge">
              <FontAwesomeIcon icon={faShieldAlt} />
              <span>Secure Chat</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Messages Section */}
      <div className="messages-container">
        <div className="chat-date-divider">
          <span>Today</span>
        </div>

        {/* Welcome Message */}
        <div className="welcome-message">
          <div className="bot-avatar">
            <FontAwesomeIcon icon={faRobot} />
          </div>
          <div className="message-content">
            <div className="message-bubble">
              <p>Hello! I'm here to support you. Feel free to share what's on your mind.</p>
              <div className="message-footer">
                <span className="message-time">Now</span>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.sender === 'bot' && (
              <div className="bot-avatar">
                <FontAwesomeIcon icon={faRobot} />
              </div>
            )}
            <div className="message-content">
              <div className="message-bubble">
                <p>{message.text}</p>
                <div className="message-footer">
                  <span className="message-time">{message.timestamp}</span>
                  {message.sender === 'user' && (
                    <span className="message-status">Sent</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="message bot">
            <div className="bot-avatar">
              <FontAwesomeIcon icon={faRobot} />
            </div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Section */}
      <div className="chat-footer">
        <form onSubmit={sendMessage} className="input-form">
          <div className="input-actions">
            <button 
              type="button"
              className="action-button"
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
            >
              <FontAwesomeIcon icon={faSmile} />
            </button>
            <input
              type="file"
              ref={fileInputRef}
              style={{ display: 'none' }}
              onChange={handleFileUpload}
            />
            <button 
              type="button"
              className="action-button"
              onClick={() => fileInputRef.current.click()}
            >
              <FontAwesomeIcon icon={faPaperclip} />
            </button>
          </div>
          
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message here..."
          />
          
          <button type="submit" className="send-button">
            <FontAwesomeIcon icon={faPaperPlane} />
          </button>
        </form>
        
        {showEmojiPicker && (
          <div className="emoji-picker">
            {emojis.map((emoji, index) => (
              <button 
                key={index}
                onClick={() => handleEmojiClick(emoji)}
                className="emoji-button"
              >
                {emoji}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Chatbot; 