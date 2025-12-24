import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../constants/api';

export function useAuth() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check localStorage for token
    const token = localStorage.getItem('auth_token');
    const email = localStorage.getItem('user_email');
    if (token && email) {
      setUser({ token, email });
    }
  }, []);

  const login = async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) throw new Error('Login failed');

    const data = await response.json();
    localStorage.setItem('auth_token', data.access_token);
    localStorage.setItem('user_email', email);
    setUser({ token: data.access_token, email });
  };

  const signup = async (email, password, python_knowledge, has_nvidia_gpu) => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, python_knowledge, has_nvidia_gpu }),
    });

    if (!response.ok) throw new Error('Signup failed');

    const data = await response.json();
    localStorage.setItem('auth_token', data.access_token);
    localStorage.setItem('user_email', email);
    setUser({ token: data.access_token, email });
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_email');
    setUser(null);
  };

  return { user, login, signup, logout, isAuthenticated: !!user };
}