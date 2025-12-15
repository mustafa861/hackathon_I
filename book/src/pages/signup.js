import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useNavigate } from '@docusaurus/router';
import styles from './signup.module.css';

const SignupPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    software_hardware_background: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
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
      const response = await fetch('/api/auth/signup', {  // Using relative path assuming proxy setup
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Signup failed');
      }

      const result = await response.json();
      setSuccess(true);

      // Optionally, automatically sign in the user after successful signup
      // For now, we'll just redirect to sign in page after a short delay
      setTimeout(() => {
        navigate('/signin');
      }, 2000);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create an account for Physical AI & Humanoid Robotics book">
      <div className={styles.signupContainer}>
        <div className={styles.signupForm}>
          <h1>Create an Account</h1>
          <p>Join to access personalized content features</p>

          {error && <div className={styles.error}>{error}</div>}
          {success && <div className={styles.success}>Account created successfully! Redirecting to sign in...</div>}

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
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
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
                minLength="6"
                disabled={loading}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="software_hardware_background">Software/Hardware Background (Optional)</label>
              <textarea
                id="software_hardware_background"
                name="software_hardware_background"
                value={formData.software_hardware_background}
                onChange={handleChange}
                placeholder="e.g., Robotics engineer, AI researcher, Student studying computer science, etc."
                disabled={loading}
              />
            </div>

            <button type="submit" className={styles.signupButton} disabled={loading}>
              {loading ? 'Creating Account...' : 'Sign Up'}
            </button>
          </form>

          <div className={styles.loginLink}>
            Already have an account? <a href="/signin">Sign in here</a>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SignupPage;