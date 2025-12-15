import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useNavigate } from '@docusaurus/router';
import styles from './signin.module.css';

const SigninPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('/api/auth/signin', {  // Using relative path assuming proxy setup
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Signin failed');
      }

      const result = await response.json();

      // Store the token in localStorage (or sessionStorage) for use in other components
      localStorage.setItem('access_token', result.access_token);

      // Redirect to homepage or a protected page after successful signin
      navigate('/');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to your Physical AI & Humanoid Robotics account">
      <div className={styles.signinContainer}>
        <div className={styles.signinForm}>
          <h1>Sign In to Your Account</h1>
          <p>Access personalized content features</p>

          {error && <div className={styles.error}>{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className={styles.formGroup}>
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>

            <button type="submit" className={styles.signinButton} disabled={loading}>
              {loading ? 'Signing In...' : 'Sign In'}
            </button>
          </form>

          <div className={styles.signupLink}>
            Don't have an account? <a href="/signup">Sign up here</a>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SigninPage;