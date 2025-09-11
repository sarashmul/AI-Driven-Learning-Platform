import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, setAuthToken, setCurrentUser, getCurrentUser, getAuthToken } from '../services/api';

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
      
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed';
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
      
      return { success: true };
    } catch (error) {
      console.error('Registration error:', error);
      let message = 'Registration failed';
      
      if (error.response?.data) {
        if (error.response.data.detail) {
          message = typeof error.response.data.detail === 'string' 
            ? error.response.data.detail 
            : 'Validation error - please check your input';
        } else if (error.response.data.message) {
          message = error.response.data.message;
        }
      }
      
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
