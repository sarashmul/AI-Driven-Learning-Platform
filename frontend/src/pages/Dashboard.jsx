import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  Chip,
  Paper,
  Divider,
} from '@mui/material';
import {
  AutoAwesome,
  Category,
  Send,
  History,
  TrendingUp,
} from '@mui/icons-material';
import { categoriesAPI, promptsAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const [categories, setCategories] = useState([]);
  const [subCategories, setSubCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedSubCategory, setSelectedSubCategory] = useState('');
  const [prompt, setPrompt] = useState('');
  const [generatedLesson, setGeneratedLesson] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [recentPrompts, setRecentPrompts] = useState([]);

  const { user } = useAuth();

  useEffect(() => {
    loadCategories();
    loadRecentPrompts();
  }, []);

  useEffect(() => {
    if (selectedCategory) {
      loadSubCategories(selectedCategory);
      setSelectedSubCategory('');
    }
  }, [selectedCategory]);

  const loadCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories(response.data);
    } catch (error) {
      setError('Failed to load categories');
    }
  };

  const loadSubCategories = async (categoryId) => {
    try {
      const response = await categoriesAPI.getSubCategories(categoryId);
      setSubCategories(response.data);
    } catch (error) {
      setError('Failed to load subcategories');
    }
  };

  const loadRecentPrompts = async () => {
    try {
      const response = await promptsAPI.getUserPrompts();
      setRecentPrompts(response.data.slice(0, 3)); // Get latest 3 prompts
    } catch (error) {
      console.error('Failed to load recent prompts');
    }
  };

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
    setError('');
  };

  const handleSubCategoryChange = (event) => {
    setSelectedSubCategory(event.target.value);
    setError('');
  };

  const handlePromptChange = (event) => {
    setPrompt(event.target.value);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedCategory || !selectedSubCategory || !prompt || !prompt.trim() || prompt.trim().length < 10) {
      setError('Please fill in all fields and ensure prompt is at least 10 characters');
      return;
    }

    setSubmitting(true);
    setError('');
    setSuccess('');
    setGeneratedLesson('');

    try {
      const response = await promptsAPI.create(
        prompt.trim(),
        selectedCategory,
        selectedSubCategory
      );
      
      setGeneratedLesson(response.data.response);
      setSuccess('Lesson generated successfully!');
      
      // Reset form
      setPrompt('');
      setSelectedCategory('');
      setSelectedSubCategory('');
      setSubCategories([]);
      
      // Reload recent prompts
      loadRecentPrompts();
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to generate lesson';
      setError(message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
          AI Learning Dashboard
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Welcome back, {user?.full_name}! Ready to learn something new today?
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {/* Main Learning Form */}
        <Grid size={{ xs: 12, md: 8 }}>
          <Card elevation={3}>
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <AutoAwesome sx={{ mr: 2, color: 'primary.main', fontSize: 32 }} />
                <Typography variant="h5" component="h2" sx={{ fontWeight: 600 }}>
                  Generate Your Lesson
                </Typography>
              </Box>

              {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  {error}
                </Alert>
              )}

              {success && (
                <Alert severity="success" sx={{ mb: 3 }}>
                  {success}
                </Alert>
              )}

              <Box component="form" onSubmit={handleSubmit}>
                <Grid container spacing={3}>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <FormControl fullWidth>
                      <InputLabel id="category-label">
                        <Category sx={{ mr: 1, fontSize: 16 }} />
                        Category
                      </InputLabel>
                      <Select
                        labelId="category-label"
                        value={selectedCategory}
                        label="Category"
                        onChange={handleCategoryChange}
                        disabled={loading || submitting}
                      >
                        {categories.map((category) => (
                          <MenuItem key={category.id} value={category.id}>
                            {category.name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>

                  <Grid size={{ xs: 12, sm: 6 }}>
                    <FormControl fullWidth>
                      <InputLabel id="subcategory-label">Sub-Category</InputLabel>
                      <Select
                        labelId="subcategory-label"
                        value={selectedSubCategory}
                        label="Sub-Category"
                        onChange={handleSubCategoryChange}
                        disabled={!selectedCategory || loading || submitting}
                      >
                        {subCategories.map((subCategory) => (
                          <MenuItem key={subCategory.id} value={subCategory.id}>
                            {subCategory.name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>

                  <Grid size={{ xs: 12 }}>
                    <TextField
                      fullWidth
                      multiline
                      rows={4}
                      label="What would you like to learn about?"
                      placeholder="Enter your learning prompt here... (e.g., 'Explain the basics of machine learning')"
                      value={prompt}
                      onChange={handlePromptChange}
                      disabled={submitting}
                      sx={{ mb: 2 }}
                    />
                  </Grid>

                  <Grid size={{ xs: 12 }}>
                    <Button
                      type="submit"
                      variant="contained"
                      size="large"
                      startIcon={submitting ? <CircularProgress size={20} /> : <Send />}
                      disabled={submitting || !selectedCategory || !selectedSubCategory || !prompt.trim()}
                      sx={{ 
                        py: 1.5,
                        px: 4,
                        fontSize: '1.1rem',
                        fontWeight: 600,
                      }}
                    >
                      {submitting ? 'Generating Lesson...' : 'Generate Lesson'}
                    </Button>
                  </Grid>
                </Grid>
              </Box>

              {/* Generated Lesson Display */}
              {generatedLesson && (
                <Box sx={{ mt: 4 }}>
                  <Divider sx={{ mb: 3 }} />
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    Your Generated Lesson
                  </Typography>
                  <Paper 
                    elevation={1} 
                    sx={{ 
                      p: 3, 
                      backgroundColor: 'grey.50',
                      borderLeft: 4,
                      borderColor: 'primary.main',
                    }}
                  >
                    <Typography 
                      variant="body1" 
                      sx={{ 
                        lineHeight: 1.8,
                        whiteSpace: 'pre-wrap',
                      }}
                    >
                      {generatedLesson}
                    </Typography>
                  </Paper>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Sidebar */}
        <Grid size={{ xs: 12, md: 4 }}>
          {/* Quick Stats */}
          <Card elevation={3} sx={{ mb: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUp sx={{ mr: 2, color: 'secondary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Quick Stats
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Total Lessons
                </Typography>
                <Chip 
                  label={recentPrompts.length} 
                  color="primary" 
                  size="small"
                />
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2" color="text.secondary">
                  Learning Streak
                </Typography>
                <Chip 
                  label="🔥 Active" 
                  color="secondary" 
                  size="small"
                />
              </Box>
            </CardContent>
          </Card>

          {/* Recent Learning History */}
          <Card elevation={3}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <History sx={{ mr: 2, color: 'secondary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Recent Lessons
                </Typography>
              </Box>
              
              {recentPrompts.length > 0 ? (
                recentPrompts.map((prompt, index) => (
                  <Box key={prompt.id} sx={{ mb: 2 }}>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      {prompt.prompt ? prompt.prompt.substring(0, 60) + '...' : 'No content'}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(prompt.created_at).toLocaleDateString()}
                    </Typography>
                    {index < recentPrompts.length - 1 && <Divider sx={{ mt: 1 }} />}
                  </Box>
                ))
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No recent lessons yet. Create your first lesson above!
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
