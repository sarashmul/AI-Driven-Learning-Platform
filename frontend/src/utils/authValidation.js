// Error message mappings for better UX
export const AUTH_ERROR_MESSAGES = {
  // Login errors
  'Invalid credentials': 'Invalid email or password. Please try again.',
  'User not found': 'User not found. Would you like to register instead?',
  'Incorrect password': 'Incorrect password. Please try again.',
  'Account locked': 'Account temporarily locked. Please contact support.',
  'Account not verified': 'Account not verified. Please check your email.',
  
  // Registration errors
  'Email already registered': 'Email already registered. Would you like to sign in instead?',
  'User already exists': 'User already exists. Please sign in or use a different email.',
  'Invalid email format': 'Invalid email format. Please enter a valid email.',
  'Password too weak': 'Password too weak. Please use a stronger password.',
  'Password too short': 'Password too short. At least 8 characters required.',
  'Name too short': 'Name too short. At least 2 characters required.',
  'Name contains invalid characters': 'Name contains invalid characters. Use letters and numbers only.',
  
  // Network errors
  'Network Error': 'Connection problem. Please check your internet connection and try again.',
  'Request timeout': 'Request took too long. Please try again.',
  'Server error': 'Server error. Please try again later.',
  
  // Default messages
  'default_login': 'Login failed. Please check your details and try again.',
  'default_register': 'Registration failed. Please check your details and try again.',
  'default_network': 'Network error. Please check your internet connection and try again.',
};

// Success messages
export const AUTH_SUCCESS_MESSAGES = {
  'login': 'Login successful! Redirecting to dashboard...',
  'register': 'Registration successful! Welcome to the learning platform!',
  'logout': 'Logged out successfully. Thank you for using our platform!',
};

// Input validation messages
export const VALIDATION_MESSAGES = {
  'email_required': 'Email is required',
  'email_invalid': 'Invalid email format',
  'password_required': 'Password is required',
  'password_min_length': 'Password must be at least 8 characters',
  'password_complexity': 'Password must contain uppercase, lowercase, and number',
  'passwords_not_match': 'Passwords do not match',
  'name_required': 'Name is required',
  'name_min_length': 'Name must be at least 2 characters',
  'name_max_length': 'Name can be up to 50 characters',
  'name_english_only': 'Name must contain only English letters and spaces',
  'confirm_password_required': 'Password confirmation is required',
};

// Helper function to get user-friendly error message
export const getErrorMessage = (error, type = 'login') => {
  // Handle different error structures
  let errorMessage = '';
  
  if (typeof error === 'string') {
    errorMessage = error;
  } else if (error?.response?.data?.detail) {
    if (typeof error.response.data.detail === 'string') {
      errorMessage = error.response.data.detail;
    } else if (Array.isArray(error.response.data.detail)) {
      // Handle validation errors array
      errorMessage = error.response.data.detail.map(err => err.msg || err.message || err).join(', ');
    }
  } else if (error?.response?.data?.message) {
    errorMessage = error.response.data.message;
  } else if (error?.message) {
    errorMessage = error.message;
  }

  // Handle specific HTTP status codes
  if (error?.response?.status) {
    switch (error.response.status) {
      case 401:
        return type === 'login' ? 'Invalid email or password. Please try again.' : 'Authentication failed. Please try again.';
      case 409:
        return 'Email already registered. Would you like to sign in instead?';
      case 422:
        // Validation error - try to extract specific field errors
        if (errorMessage.toLowerCase().includes('email')) {
          return 'Invalid email format. Please enter a valid email address.';
        }
        if (errorMessage.toLowerCase().includes('password')) {
          return 'Password requirements not met. Please ensure it meets the criteria.';
        }
        if (errorMessage.toLowerCase().includes('name')) {
          return 'Invalid name format. Please use only English letters and spaces.';
        }
        return 'Please check your input and try again.';
      case 400:
        if (errorMessage.toLowerCase().includes('email')) {
          return 'Invalid email format. Please enter a valid email address.';
        }
        if (errorMessage.toLowerCase().includes('password')) {
          return 'Password requirements not met. Please check the criteria below.';
        }
        return 'Invalid input. Please check your information and try again.';
      case 500:
        return 'Server error. Please try again later.';
      case 503:
        return 'Service temporarily unavailable. Please try again later.';
    }
  }

  // Map specific error messages to user-friendly ones
  const lowerErrorMessage = errorMessage.toLowerCase();
  
  // Email related errors
  if (lowerErrorMessage.includes('email already exists') || lowerErrorMessage.includes('email already registered')) {
    return AUTH_ERROR_MESSAGES['Email already registered'];
  }
  if (lowerErrorMessage.includes('user already exists')) {
    return AUTH_ERROR_MESSAGES['User already exists'];
  }
  if (lowerErrorMessage.includes('invalid email')) {
    return AUTH_ERROR_MESSAGES['Invalid email format'];
  }
  
  // Password related errors
  if (lowerErrorMessage.includes('invalid credentials') || lowerErrorMessage.includes('incorrect password')) {
    return AUTH_ERROR_MESSAGES['Invalid credentials'];
  }
  if (lowerErrorMessage.includes('password too weak') || lowerErrorMessage.includes('password requirements')) {
    return AUTH_ERROR_MESSAGES['Password too weak'];
  }
  if (lowerErrorMessage.includes('password too short')) {
    return AUTH_ERROR_MESSAGES['Password too short'];
  }
  
  // User related errors
  if (lowerErrorMessage.includes('user not found')) {
    return AUTH_ERROR_MESSAGES['User not found'];
  }
  
  // Network errors
  if (lowerErrorMessage.includes('network error') || error?.code === 'NETWORK_ERROR') {
    return AUTH_ERROR_MESSAGES['default_network'];
  }
  if (lowerErrorMessage.includes('timeout')) {
    return AUTH_ERROR_MESSAGES['Request timeout'];
  }

  // Use mapped message if available
  if (AUTH_ERROR_MESSAGES[errorMessage]) {
    return AUTH_ERROR_MESSAGES[errorMessage];
  }

  // Default fallback messages based on type
  if (type === 'register') {
    return AUTH_ERROR_MESSAGES['default_register'];
  }
  
  return AUTH_ERROR_MESSAGES['default_login'];
};

// Email validation
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Password validation
export const validatePassword = (password) => {
  const minLength = password.length >= 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  
  return {
    isValid: minLength && hasUpperCase && hasLowerCase && hasNumbers,
    requirements: {
      minLength,
      hasUpperCase,
      hasLowerCase,
      hasNumbers,
    }
  };
};

// Name validation - English only
export const validateName = (name) => {
  if (!name || name.trim().length < 2) {
    return { isValid: false, message: VALIDATION_MESSAGES.name_min_length };
  }
  if (name.length > 50) {
    return { isValid: false, message: VALIDATION_MESSAGES.name_max_length };
  }
  
  // Allow only English letters, spaces, hyphens, and apostrophes
  const englishNameRegex = /^[a-zA-Z\s'-]+$/;
  if (!englishNameRegex.test(name)) {
    return { 
      isValid: false, 
      message: VALIDATION_MESSAGES.name_english_only
    };
  }
  
  return { isValid: true };
};