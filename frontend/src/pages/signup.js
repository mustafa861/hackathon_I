import React, { useState } from 'react';
import Layout from '@theme/Layout';

export default function SignupPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    pythonKnowledge: false,
    hasNvidiaGpu: false
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
      const response = await fetch('http://localhost:8000/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
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

              <div className="margin-bottom--sm">
                <label>
                  <input
                    type="checkbox"
                    name="pythonKnowledge"
                    checked={formData.pythonKnowledge}
                    onChange={handleChange}
                  />
                  {' '}Do you know Python?
                </label>
              </div>

              <div className="margin-bottom--sm">
                <label>
                  <input
                    type="checkbox"
                    name="hasNvidiaGpu"
                    checked={formData.hasNvidiaGpu}
                    onChange={handleChange}
                  />
                  {' '}Do you have an NVIDIA GPU?
                </label>
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