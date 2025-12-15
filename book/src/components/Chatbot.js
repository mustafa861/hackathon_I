import React, { useState, useRef, useEffect } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import './Chatbot.css'; // Import the CSS file for styling

const Chatbot = ({ backendUrl = 'http://localhost:8000' }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [showSelectedTextButton, setShowSelectedTextButton] = useState(false);
  const [selectedTextButtonPosition, setSelectedTextButtonPosition] = useState({ x: 0, y: 0 });
  const messagesEndRef = useRef(null);
  const { colorMode } = useColorMode();
  const isDarkMode = colorMode === 'dark';

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Effect to handle text selection on the page
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text) {
        // Get the position for the button (near the end of the selection)
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        setSelectedTextButtonPosition({ x: rect.right - 30, y: rect.top - 40 });
        setShowSelectedTextButton(true);
        setSelectedText(text);
      } else {
        setShowSelectedTextButton(false);
      }
    };

    const handleMouseUp = () => {
      setTimeout(handleSelection, 0); // Use setTimeout to ensure selection is complete
    };

    const handleClickOutside = (e) => {
      // If the click is outside the selected text button, hide it
      if (!e.target.closest('.selected-text-button')) {
        setShowSelectedTextButton(false);
      }
    };

    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('click', handleClickOutside);

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);

  const handleSubmit = async (e, contextText = '') => {
    e.preventDefault();
    if (!inputValue.trim() && !contextText.trim() || isLoading) return;

    // Create the query with context if available
    const query = contextText ? `${contextText}\n\nQuestion: ${inputValue}` : inputValue;

    // Add user message to the chat
    const userMessage = {
      sender: 'user',
      text: inputValue,
      context: contextText, // Store context separately for display
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await fetch(`${backendUrl}/api/chatbot/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          top_k: 5
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      // Add bot response to the chat
      const botMessage = {
        sender: 'bot',
        text: data.response,
        contexts: data.contexts, // Include context information
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        sender: 'bot',
        text: `Sorry, I encountered an error: ${error.message}. Please try again.`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      // Hide the selected text button after submission
      setShowSelectedTextButton(false);
      setSelectedText('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleUseSelectedText = (e) => {
    e.preventDefault();
    // Pre-fill the input with the selected text and add a question prompt
    setInputValue(`Regarding this text: "${selectedText}" `);
    setShowSelectedTextButton(false);
    setSelectedText('');
  };

  return (
    <div className={`chatbot-container ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <div className="chatbot-header">
        <h3>AI Assistant for Physical AI & Humanoid Robotics</h3>
      </div>
      <div className="chatbot-messages">
        {messages.length === 0 ? (
          <div className="chatbot-welcome-message">
            <p>Hello! I'm your AI assistant for the "Physical AI & Humanoid Robotics" book.</p>
            <p>Ask me anything about the content in this book, and I'll do my best to help!</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <div className="message-content">
                <p>{msg.text}</p>
                {msg.context && (
                  <details className="context-details">
                    <summary>Selected Text Context</summary>
                    <p>{msg.context}</p>
                  </details>
                )}
                {msg.contexts && msg.contexts.length > 0 && (
                  <details className="context-details">
                    <summary>Context Used from Book</summary>
                    <ul>
                      {msg.contexts.map((context, idx) => (
                        <li key={idx} className="context-item">
                          <strong>{context.title}</strong>: {context.content.substring(0, 100)}...
                        </li>
                      ))}
                    </ul>
                  </details>
                )}
              </div>
              <span className="timestamp">
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot">
            <div className="message-content">
              <p>Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form className="chatbot-input-form" onSubmit={handleSubmit}>
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the book content..."
          rows="2"
          disabled={isLoading}
          className="chatbot-input"
        />
        <button type="submit" disabled={isLoading} className="chatbot-send-button">
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>

      {/* Floating button to use selected text */}
      {showSelectedTextButton && (
        <button
          className="selected-text-button"
          style={{
            position: 'fixed',
            left: `${selectedTextButtonPosition.x}px`,
            top: `${selectedTextButtonPosition.y}px`,
            zIndex: 10000,
            backgroundColor: '#25c2a0',
            color: 'white',
            border: 'none',
            borderRadius: '50%',
            width: '40px',
            height: '40px',
            cursor: 'pointer',
            fontSize: '16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
          }}
          onClick={handleUseSelectedText}
          title="Ask about selected text"
        >
          💬
        </button>
      )}
    </div>
  );
};

export default Chatbot;