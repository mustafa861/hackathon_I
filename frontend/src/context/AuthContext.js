import React, { createContext, useContext, useReducer, useEffect } from 'react';

const AuthContext = createContext();

const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload
      };
    default:
      return state;
  }
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    token: null,
    isAuthenticated: false,
    loading: true
  });

  useEffect(() => {
    // Check for existing token on app start
    // Use consistent keys with the useAuth hook: 'auth_token' and 'user_email'
    const token = localStorage.getItem('auth_token');
    const email = localStorage.getItem('user_email');

    if (token && email) {
      const userData = { email }; // Create user object from email
      dispatch({
        type: 'LOGIN',
        payload: { user: userData, token }
      });
    }
    dispatch({ type: 'SET_LOADING', payload: false });
  }, []);

  const login = (userData, token) => {
    // Use consistent keys with the useAuth hook: 'auth_token' and 'user_email'
    localStorage.setItem('auth_token', token);
    localStorage.setItem('user_email', userData.email);
    dispatch({
      type: 'LOGIN',
      payload: { user: userData, token }
    });
  };

  const logout = () => {
    // Use consistent keys with the useAuth hook: 'auth_token' and 'user_email'
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_email');
    dispatch({ type: 'LOGOUT' });
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};