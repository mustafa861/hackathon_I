import React from 'react';
import { useAuth } from '@site/src/context/AuthContext';
import clsx from 'clsx';

const AuthNavbar = () => {
  const { user, logout, isAuthenticated } = useAuth();

  if (isAuthenticated && user) {
    // Show user email and logout button when authenticated
    return (
      <div className={clsx('navbar__item', 'navbar__user-info')}>
        <span className="navbar__user-email" style={{ marginRight: '1rem', color: 'white' }}>
          {user.email}
        </span>
        <button
          className="navbar__logout-button"
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            textDecoration: 'underline',
            fontSize: '0.875rem'
          }}
          onClick={logout}
        >
          Logout
        </button>
      </div>
    );
  } else {
    // Show signup and login links when not authenticated
    return (
      <div className={clsx('navbar__item', 'navbar__auth-links')}>
        <a
          href="/signup"
          className="navbar__link"
          style={{ marginRight: '1rem', color: 'white' }}
        >
          Sign Up
        </a>
        <a
          href="/login"
          className="navbar__link"
          style={{ color: 'white' }}
        >
          Login
        </a>
      </div>
    );
  }
};

export default AuthNavbar;