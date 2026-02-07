import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { API_BASE_URL } from '../constants/api';

export function ChatWidget() {
  const { user, isAuthenticated, login } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!query.trim()) return;

    setMessages(prev => [...prev, { role: 'user', content: query }]);
    setLoading(true);

    try {
      // Create a simple request without authentication for guest users
      const requestBody = {
        query,
        selected_context: '',
      };

      // Include user info if available, otherwise proceed as guest
      const headers = { 'Content-Type': 'application/json' };
      if (isAuthenticated && user && user.token) {
        headers['Authorization'] = `Bearer ${user.token}`;
      }
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify(requestBody),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        const msg = data.answer || (response.status === 404
          ? `Chat endpoint not found. Is the backend running at ${API_BASE_URL}?`
          : 'Error occurred while processing your request.');
        setMessages(prev => [...prev, { role: 'assistant', content: msg }]);
        return;
      }
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error occurred while processing your request.' }]);
    } finally {
      setLoading(false);
      setQuery('');
    }
  };

  return (
    <div style={{ position: 'fixed', bottom: '20px', right: '20px', zIndex: 1000 }}>
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          style={{
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            backgroundColor: '#000000',
            color: 'white',
            border: '1px solid #000000',
            fontSize: '24px',
            cursor: 'pointer',
          }}
        >
          💬
        </button>
      ) : (
        <div style={{
          width: '350px',
          height: '500px',
          backgroundColor: 'white',
          borderRadius: '10px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          display: 'flex',
          flexDirection: 'column',
          border: '1px solid black',
        }}>
          <div style={{ padding: '15px', borderBottom: '1px solid #ddd', display: 'flex', justifyContent: 'space-between', backgroundColor: '#000000', color: 'white' }}>
            <span style={{ fontWeight: 'bold' }}>Textbook Assistant</span>
            <button onClick={() => setIsOpen(false)} style={{ border: 'none', background: 'none', cursor: 'pointer', color: 'white', fontSize: '18px' }}>✕</button>
          </div>

          <div style={{ flex: 1, overflowY: 'auto', padding: '15px', backgroundColor: '#ffffff', color: 'black' }}>
            {messages.map((msg, idx) => (
              <div key={idx} style={{ marginBottom: '10px', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                <div style={{
                  display: 'inline-block',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  backgroundColor: msg.role === 'user' ? '#000000' : '#f0f0f0',
                  color: msg.role === 'user' ? 'white' : 'black',
                  maxWidth: '80%',
                }}>
                  {msg.content}
                </div>
              </div>
            ))}
          </div>

          <div style={{ padding: '15px', borderTop: '1px solid #ddd', display: 'flex', backgroundColor: '#ffffff' }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
              placeholder="Ask a question..."
              style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #000000', backgroundColor: '#ffffff', color: 'black' }}
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              style={{ marginLeft: '10px', padding: '8px 15px', borderRadius: '4px', backgroundColor: '#000000', color: 'white', border: '1px solid #000000' }}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}