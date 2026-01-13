import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../constants/api';

interface User {
  token: string;
  email: string;
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Check localStorage for token - use the same keys as AuthContext
    const token = localStorage.getItem('auth_token');
    const email = localStorage.getItem('user_email');
    if (token && email) {
      setUser({ token, email });
    }
  }, []);

  const login = async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) throw new Error('Login failed');

    const data = await response.json();
    // Use consistent keys with AuthContext
    localStorage.setItem('auth_token', data.access_token);
    localStorage.setItem('user_email', email);
    setUser({ token: data.access_token, email });
  };

  const signup = async (email: string, password: string, python_knowledge: boolean, has_nvidia_gpu: boolean) => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, python_knowledge, has_nvidia_gpu }),
    });

    if (!response.ok) throw new Error('Signup failed');

    const data = await response.json();
    // Use consistent keys with AuthContext
    localStorage.setItem('auth_token', data.access_token);
    localStorage.setItem('user_email', email);
    setUser({ token: data.access_token, email });
  };

  const logout = () => {
    // Use consistent keys with AuthContext
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_email');
    setUser(null);
  };

  return { user, login, signup, logout, isAuthenticated: !!user };
}