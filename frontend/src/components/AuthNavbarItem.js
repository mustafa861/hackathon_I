import React from 'react';
import { useAuth } from '../hooks/useAuth';

const AuthNavbarItem = () => {
  const { user, logout, isAuthenticated } = useAuth();

  if (isAuthenticated && user) {
    // Show user email and logout button when authenticated
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <span style={{ color: 'white', fontSize: '0.875rem' }}>
          {user.email}
        </span>
        <button
          onClick={logout}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            textDecoration: 'underline',
            fontSize: '0.875rem',
            padding: 0,
            margin: 0
          }}
        >
          Logout
        </button>
      </div>
    );
  } else {
    // Show "SIGNUP" and "SIGNIN" buttons when not authenticated
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <a
          href="/signup"
          style={{
            color: 'white',
            textDecoration: 'none',
            fontSize: '0.875rem',
            padding: '6px 12px',
            border: '1px solid white',
            borderRadius: '4px',
            display: 'inline-block'
          }}
        >
          SIGNUP
        </a>
        <a
          href="/login"
          style={{
            color: 'white',
            textDecoration: 'none',
            fontSize: '0.875rem',
            padding: '6px 12px',
            border: '1px solid white',
            borderRadius: '4px',
            display: 'inline-block'
          }}
        >
          SIGNIN
        </a>
      </div>
    );
  }
};

export default AuthNavbarItem;