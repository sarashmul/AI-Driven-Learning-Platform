import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001',
  timeout: import.meta.env.VITE_API_TIMEOUT || 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  register: (userData) => api.post('/api/auth/register', userData),
  login: (credentials) => api.post('/api/auth/login', credentials),
  getProfile: () => api.get('/api/auth/me'),
};

// Categories API calls
export const categoriesAPI = {
  getAll: () => api.get('/api/categories/'),
  getById: (id) => api.get(`/api/categories/${id}`),
  getSubCategories: (categoryId) => api.get(`/api/categories/${categoryId}/subcategories`),
};

// Prompts API calls
// export const promptsAPI = {
//   create: (promptData) => api.post('/api/prompts/', promptData),
//   getUserPrompts: () => api.get('/api/prompts/my-history'),
//   getById: (id) => api.get(`/api/prompts/${id}`),
// };

// Prompts API calls
export const promptsAPI = {
  create: (text, categoryId = null, subCategoryId = null) =>
    api.post('/api/prompts/', {
      prompt: text,                 // השם הנכון שה־backend מצפה לו
      category_id: categoryId,      // אופציונלי
      sub_category_id: subCategoryId // אופציונלי
    }),
  getUserPrompts: () => api.get('/api/prompts/my-history'),
  getStats: () => api.get('/api/prompts/my-stats'),
  getById: (id) => api.get(`/api/prompts/${id}`),
};

// Admin API calls
export const adminAPI = {
  getUsers: () => api.get('/api/admin/users'),
  getUserById: (id) => api.get(`/api/admin/users/${id}`),
  updateUser: (id, userData) => api.put(`/api/admin/users/${id}`, userData),
  deleteUser: (id) => api.delete(`/api/admin/users/${id}`),
  getPrompts: () => api.get('/api/admin/prompts'),
  getPromptById: (id) => api.get(`/api/admin/prompts/${id}`),
  updatePrompt: (id, promptData) => api.put(`/api/admin/prompts/${id}`, promptData),
  deletePrompt: (id) => api.delete(`/api/admin/prompts/${id}`),
  createCategory: (categoryData) => api.post('/api/admin/categories', categoryData),
  updateCategory: (id, categoryData) => api.put(`/api/admin/categories/${id}`, categoryData),
  deleteCategory: (id) => api.delete(`/api/admin/categories/${id}`),
  createSubCategory: (subCategoryData) => api.post('/api/admin/subcategories', subCategoryData),
  updateSubCategory: (id, subCategoryData) => api.put(`/api/admin/subcategories/${id}`, subCategoryData),
  deleteSubCategory: (id) => api.delete(`/api/admin/subcategories/${id}`),
};

// Helper functions
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('token', token);
  } else {
    localStorage.removeItem('token');
  }
};

export const getAuthToken = () => {
  return localStorage.getItem('token');
};

export const isAuthenticated = () => {
  return !!getAuthToken();
};

export const getCurrentUser = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};

export const setCurrentUser = (user) => {
  if (user) {
    localStorage.setItem('user', JSON.stringify(user));
  } else {
    localStorage.removeItem('user');
  }
};

export default api;
