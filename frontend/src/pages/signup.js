import React, { useState } from 'react';
import Layout from '@theme/Layout';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function SignupPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    python_knowledge: false,
    has_nvidia_gpu: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
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
        python_knowledge: formData.python_knowledge,
        has_nvidia_gpu: formData.has_nvidia_gpu
      })
      });

      if (response.ok) {
        const data = await response.json();
        // Store token and user info in localStorage - will be picked up by AuthContext
        localStorage.setItem('auth_token', data.access_token);
        localStorage.setItem('user_email', formData.email);
        // Show success message before redirecting
        alert('Account created successfully! You are now logged in.');
        // Redirect to home page
        window.location.href = '/';
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Signup failed' }));
        alert(errorData.detail || 'Signup failed');
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

              {/* <div className="margin-bottom--sm">
                <label>
                  <input
                    type="checkbox"
                    name="python_knowledge"
                    checked={formData.python_knowledge}
                    onChange={handleChange}
                    className="margin-right--sm"
                  />
                  I have Python knowledge
                </label>
              </div>

              <div className="margin-bottom--sm">
                <label>
                  <input
                    type="checkbox"
                    name="has_nvidia_gpu"
                    checked={formData.has_nvidia_gpu}
                    onChange={handleChange}
                    className="margin-right--sm"
                  />
                  I have an NVIDIA GPU
                </label>
              </div> */}

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