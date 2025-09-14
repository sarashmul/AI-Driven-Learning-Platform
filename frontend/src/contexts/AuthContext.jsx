import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, setAuthToken, setCurrentUser, getCurrentUser, getAuthToken } from '../services/api';
import { getErrorMessage, AUTH_SUCCESS_MESSAGES } from '../utils/authValidation';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const logout = () => {
    setAuthToken(null);
    setCurrentUser(null);
    setUser(null);
  };

  useEffect(() => {
    const initializeAuth = async () => {
      const token = getAuthToken();
      const savedUser = getCurrentUser();
      
      if (token && savedUser) {
        setUser(savedUser);
        try {
          // Verify token is still valid
          const response = await authAPI.getProfile();
          setUser(response.data);
          setCurrentUser(response.data);
        } catch (error) {
          // Token invalid, clear auth
          logout();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ email, password });
      const { access_token, user: userData } = response.data;
      
      setAuthToken(access_token);
      setCurrentUser(userData);
      setUser(userData);
      
      return { success: true, message: AUTH_SUCCESS_MESSAGES.login };
    } catch (error) {
      const message = getErrorMessage(error, 'login');
      return { success: false, error: message };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      const { access_token, user: newUser } = response.data;
      
      setAuthToken(access_token);
      setCurrentUser(newUser);
      setUser(newUser);
      
      return { success: true, message: AUTH_SUCCESS_MESSAGES.register };
    } catch (error) {
      console.error('Registration error:', error);
      const message = getErrorMessage(error, 'register');
      return { success: false, error: message };
    }
  };

  const isAdmin = () => {
    return user?.role === 'admin';
  };

  const isAuthenticated = () => {
    return !!user;
  };

  const value = {
    user,
    login,
    register,
    logout,
    isAdmin,
    isAuthenticated,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
