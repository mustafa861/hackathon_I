import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { NavbarNavLink } from '@theme/Navbar/Items';
import { translate } from '@docusaurus/Translate';

const UserInfoNavbarItem = (props) => {
  const { user, logout, isAuthenticated } = useAuth();

  if (isAuthenticated && user) {
    return (
      <div className="navbar__item navbar__user-info">
        <span className="navbar__user-email">{user.email}</span>
        <button
          className="navbar__logout-button"
          onClick={logout}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            marginLeft: '1rem',
            textDecoration: 'underline'
          }}
        >
          {translate({ id: 'theme.navbar.logout', message: 'Logout' })}
        </button>
      </div>
    );
  }

  return null; // Don't render anything if not authenticated
};

export default UserInfoNavbarItem;