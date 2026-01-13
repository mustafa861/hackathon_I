import React, { useState } from 'react';
import Layout from '@theme/Layout';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
        email: formData.email,
        password: formData.password
      })
      });

      if (response.ok) {
        const data = await response.json();
        // Store token and user info in localStorage - will be picked up by AuthContext
        localStorage.setItem('auth_token', data.access_token);
        localStorage.setItem('user_email', formData.email);
        // Redirect to home page
        window.location.href = '/';
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
        alert(errorData.detail || 'Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed');
    }
  };

  return (
    <Layout title="Login" description="Log in to the Physical AI Textbook">
      <div className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
              <div className="margin-bottom--sm">
                <label htmlFor="email">Email:</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="form-control"
                />
              </div>

              <div className="margin-bottom--sm">
                <label htmlFor="password">Password:</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="form-control"
                />
              </div>

              <button type="submit" className="button button--primary">
                Login
              </button>
            </form>
          </div>
        </div>
      </div>
    </Layout>
  );
}