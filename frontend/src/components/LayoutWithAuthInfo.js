import React from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/hooks/useAuth';

function LayoutWithAuthInfo({ children, ...props }) {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <Layout {...props}>
      {/* Show user info at the top of the page when authenticated */}
      {isAuthenticated && user && (
        <div style={{
          backgroundColor: '#000',
          color: 'white',
          padding: '8px 20px',
          display: 'flex',
          justifyContent: 'flex-end',
          alignItems: 'center',
          fontSize: '14px'
        }}>
          <span style={{ marginRight: '15px' }}>
            Welcome, {user.email}
          </span>
          <button
            onClick={logout}
            style={{
              background: 'none',
              border: '1px solid white',
              color: 'white',
              padding: '4px 12px',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Logout
          </button>
        </div>
      )}
      {children}
    </Layout>
  );
}

export default LayoutWithAuthInfo;