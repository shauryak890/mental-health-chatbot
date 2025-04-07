import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faArrowLeft, 
  faRobot, 
  faPaperPlane,
  faSmile,
  faInfoCircle,
  faShieldAlt,
  faTimesCircle,
  faHome,
  faBook,
  faHeartPulse,
  faComments,
  faTrash
} from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';

function Chatbot({ onBack }) {
  // State Management
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [showInfoPanel, setShowInfoPanel] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const [userId, setUserId] = useState(localStorage.getItem('mindfulchat_user_id') || '');
  const [conversationHistory, setConversationHistory] = useState([]);

  // Auto Scroll
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input on load
  useEffect(() => {
    inputRef.current?.focus();
    
    // Add welcome message
    if (messages.length === 0) {
      setMessages([{
        text: "Hey there! 👋 I'm your friend in this space. Having a rough day or just want to chat? I'm all ears! College life can be a lot sometimes, so whatever's on your mind, let's talk about it.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    }
  }, []);

  // Load conversation history
  useEffect(() => {
    // Retrieve conversation history if userId exists
    if (userId) {
      fetchConversationHistory();
    }
  }, [userId]);

  // Functions to interact with the backend
  const fetchConversationHistory = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/history?userId=${userId}`);
      const data = await response.json();
      
      if (data.history && data.history.length > 0) {
        // Format the history into messages
        const formattedMessages = data.history.map(msg => ({
          text: msg.text,
          sender: msg.role === 'user' ? 'user' : 'bot',
          category: msg.category || 'general',
          timestamp: msg.timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }));
        
        setMessages(formattedMessages);
      } else if (messages.length === 0) {
        // If no history and no welcome message, add the welcome message
        setMessages([{
          text: "Hey there! 👋 I'm your friend in this space. Having a rough day or just want to chat? I'm all ears! College life can be a lot sometimes, so whatever's on your mind, let's talk about it.",
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
      }
    } catch (error) {
      console.error('Error fetching conversation history:', error);
    }
  };

  const resetConversation = async () => {
    try {
      await fetch('http://localhost:5000/api/reset', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId }),
      });
      
      setMessages([{
        text: "Hey there! 👋 I'm your friend in this space. Having a rough day or just want to chat? I'm all ears! College life can be a lot sometimes, so whatever's on your mind, let's talk about it.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } catch (error) {
      console.error('Error resetting conversation:', error);
    }
  };

  // Message Handlers
  const sendMessage = async (e) => {
    e?.preventDefault();
    if (!inputMessage.trim()) return;

    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    const userMessage = {
      text: inputMessage,
      sender: 'user',
      timestamp: currentTime
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
        body: JSON.stringify({ 
          message: inputMessage,
          userId: userId,
          timestamp: currentTime
        }),
      });

      const data = await response.json();
      
      // If we got a userId, store it for future sessions
      if (data.userId && (!userId || userId !== data.userId)) {
        setUserId(data.userId);
        localStorage.setItem('mindfulchat_user_id', data.userId);
      }
      
      // Small delay to make the interaction feel more natural
      setTimeout(() => {
        const botMessage = {
          text: data.response,
          sender: 'bot',
          category: data.category,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
  
        setMessages(prev => [...prev, botMessage]);
        setIsLoading(false);
      }, 700);
    } catch (error) {
      console.error('Error:', error);
      // Add error message to chat
      setTimeout(() => {
        setMessages(prev => [...prev, {
          text: "Sorry, I'm having trouble connecting. Please try again in a moment.",
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
        setIsLoading(false);
      }, 700);
    }
  };

  // Feature Handlers
  const handleEmojiClick = (emoji) => {
    setInputMessage(prev => prev + emoji);
    setShowEmojiPicker(false);
    inputRef.current?.focus();
  };

  // Get message category color
  const getCategoryColor = (category) => {
    const colors = {
      'financial': 'var(--secondary)',
      'loneliness': 'var(--accent)',
      'academic': 'var(--primary)',
      'stress': 'var(--warning)',
      'general': 'var(--text-primary)',
      'coping_strategies': 'var(--success)',
      'positive_reinforcement': 'var(--info)',
      'validation': 'var(--primary-light)',
      'empathy': 'var(--accent-light)'
    };
    return colors[category] || 'var(--text-primary)';
  };

  // Simple emoji picker
  const emojis = ['😊', '😔', '😢', '😡', '😌', '🤔', '❤️', '👍'];

  return (
    <div className="chat-container">
      <motion.div 
        className="chat-sidebar"
        animate={{ 
          x: showInfoPanel ? 0 : '100%' 
        }}
      >
        <div className="sidebar-header">
          <div className="logo">
            <FontAwesomeIcon icon={faHeartPulse} className="logo-icon" />
            MindfulChat
          </div>
          <button className="back-button" onClick={onBack}>
            <FontAwesomeIcon icon={faArrowLeft} />
          </button>
        </div>
        <div className="sidebar-navigation">
          <Link to="/" className="nav-link" onClick={onBack}>
            <FontAwesomeIcon icon={faHome} />
            Home
          </Link>
          <Link to="/resources" className="nav-link">
            <FontAwesomeIcon icon={faBook} />
            Resources
          </Link>
        </div>
        <div className="sidebar-content">
          <div className="sidebar-section">
            <h4>How It Works</h4>
            <p>MindfulChat uses AI to provide supportive responses to your concerns. Simply share what's on your mind, and the system will offer guidance and resources.</p>
          </div>
          
          <div className="sidebar-section">
            <h4>Privacy & Security</h4>
            <p>Your conversations are confidential. We prioritize your privacy and implement strong security measures to protect your information.</p>
          </div>
          
          <div className="sidebar-section">
            <h4>Support Areas</h4>
            <ul className="support-areas-list">
              <li><span className="category-tag" style={{ backgroundColor: getCategoryColor('financial') }}>Financial</span></li>
              <li><span className="category-tag" style={{ backgroundColor: getCategoryColor('academic') }}>Academic</span></li>
              <li><span className="category-tag" style={{ backgroundColor: getCategoryColor('loneliness') }}>Social</span></li>
              <li><span className="category-tag" style={{ backgroundColor: getCategoryColor('stress') }}>Stress</span></li>
              <li><span className="category-tag" style={{ backgroundColor: getCategoryColor('general') }}>General</span></li>
            </ul>
          </div>
          
          <div className="sidebar-section">
            <h4>Important Note</h4>
            <p>MindfulChat is not a replacement for professional mental health services. If you're experiencing a crisis or emergency, please contact professional help immediately.</p>
            <p className="emergency-contact">Crisis Hotline: 988</p>
          </div>
        </div>
      </motion.div>
    
      <div className="chat-main">
        {/* Header Section */}
        <div className="chat-header">
          <button className="back-button" onClick={onBack}>
            <FontAwesomeIcon icon={faArrowLeft} />
          </button>
          
          <div className="header-content">
            <h1>MindfulChat</h1>
            <div className="status-indicator">
              <span className="status-dot"></span>
              <span>Ready to help</span>
            </div>
          </div>
          
          <div className="header-actions">
            <button 
              className="info-button"
              onClick={() => setShowInfoPanel(!showInfoPanel)}
            >
              <FontAwesomeIcon icon={faInfoCircle} />
            </button>
            <button 
              className="reset-button"
              onClick={resetConversation}
              title="Start a new conversation"
            >
              <FontAwesomeIcon icon={faTrash} />
            </button>
            <div className="security-badge">
              <FontAwesomeIcon icon={faShieldAlt} />
              <span>Secure</span>
            </div>
          </div>
        </div>
        
        {/* Messages Section */}
        <div className="messages-container">
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div 
                key={index} 
                className={`message ${message.sender}`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                {message.sender === 'bot' && (
                  <div className="bot-avatar">
                    <FontAwesomeIcon icon={faRobot} />
                  </div>
                )}
                <div className="message-content">
                  <div 
                    className="message-bubble"
                    style={{
                      borderColor: message.category ? getCategoryColor(message.category) : null
                    }}
                  >
                    <p>{message.text}</p>
                    <div className="message-footer">
                      <span className="message-time">{message.timestamp}</span>
                      {message.category && (
                        <span 
                          className="message-category"
                          style={{ backgroundColor: getCategoryColor(message.category) }}
                        >
                          {message.category}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Loading Indicator */}
          <AnimatePresence>
            {isLoading && (
              <motion.div 
                className="message bot"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
              >
                <div className="bot-avatar">
                  <FontAwesomeIcon icon={faRobot} />
                </div>
                <div className="message-content">
                  <div className="message-bubble typing-bubble">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Section */}
        <form onSubmit={sendMessage} className="chat-footer">
          <div className="input-wrapper">
            <button 
              type="button"
              className="emoji-button"
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
            >
              <FontAwesomeIcon icon={faSmile} />
            </button>
            
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message here..."
              ref={inputRef}
            />
            
            <button 
              type="submit"
              className="send-button"
              disabled={!inputMessage.trim()}
            >
              <FontAwesomeIcon icon={faPaperPlane} />
            </button>
          </div>
          
          {showEmojiPicker && (
            <div className="emoji-picker">
              {emojis.map((emoji, index) => (
                <button
                  key={index}
                  type="button" 
                  onClick={() => handleEmojiClick(emoji)}
                  className="emoji-option"
                >
                  {emoji}
                </button>
              ))}
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default Chatbot;