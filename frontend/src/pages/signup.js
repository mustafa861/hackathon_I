import React, { useState } from 'react';
import Layout from '@theme/Layout';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function SignupPage() {
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
      const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
        email: formData.email,
        password: formData.password,
        python_knowledge: false,
        has_nvidia_gpu: false
      })
      });

      if (response.ok) {
        const data = await response.json();
        // Store token and redirect
        localStorage.setItem('auth_token', data.access_token);
        localStorage.setItem('user_email', formData.email);
        window.location.href = '/docs/intro';
      } else {
        alert('Signup failed');
      }
    } catch (error) {
      console.error('Signup error:', error);
      alert('Signup failed');
    }
  };

  return (
    <Layout title="Sign Up" description="Create an account for the Physical AI Textbook">
      <div className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <h1>Sign Up</h1>
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
                Sign Up
              </button>
            </form>
          </div>
        </div>
      </div>
    </Layout>
  );
}