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
  Schedule,
} from '@mui/icons-material';
import { categoriesAPI, promptsAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import LessonDisplay from '../components/LessonDisplay';

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
  const [selectedHistoricalLesson, setSelectedHistoricalLesson] = useState('');

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
      console.log('🔍 DEBUG: Recent prompts response:', response.data);
      setRecentPrompts(response.data.slice(0, 3)); // Get latest 3 prompts
    } catch (error) {
      console.error('Failed to load recent prompts:', error);
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

  const handleHistoricalLessonClick = (lesson) => {
    setSelectedHistoricalLesson(lesson.response);
    setGeneratedLesson(''); // Clear current lesson
    setSuccess(`Displaying lesson: "${lesson.prompt.substring(0, 50)}..."`);
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
    setSelectedHistoricalLesson(''); // Clear historical lesson

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
          Welcome back, {user?.name}! Ready to learn something new today?
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
                <LessonDisplay content={generatedLesson} />
              )}

              {/* Historical Lesson Display */}
              {selectedHistoricalLesson && !generatedLesson && (
                <>
                  <Box sx={{ mt: 2, mb: 2, textAlign: 'center' }}>
                    <Button 
                      variant="outlined" 
                      size="small"
                      onClick={() => {
                        setSelectedHistoricalLesson('');
                        setSuccess('');
                      }}
                      sx={{ borderRadius: 20 }}
                    >
                      ✕ Close Historical Lesson
                    </Button>
                  </Box>
                  <LessonDisplay 
                    content={selectedHistoricalLesson} 
                    title="Historical Lesson"
                  />
                </>
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
              
              <Typography variant="caption" sx={{ mb: 2, display: 'block', color: 'text.secondary' }}>
                💡 Click on any lesson below to view it again
              </Typography>
              
              {recentPrompts.length > 0 ? (
                recentPrompts.map((prompt, index) => {
                  console.log('🔍 DEBUG: Rendering prompt:', prompt);
                  return (
                  <Box 
                    key={prompt.id} 
                    sx={{ 
                      mb: 2,
                      p: 2,
                      border: '1px solid #e0e0e0',
                      borderRadius: 2,
                      cursor: 'pointer',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        backgroundColor: 'primary.50',
                        borderColor: 'primary.main',
                        transform: 'translateY(-2px)',
                        boxShadow: '0 4px 12px rgba(25, 118, 210, 0.15)'
                      }
                    }}
                    onClick={() => handleHistoricalLessonClick(prompt)}
                  >
                    {/* Category and Subcategory first */}
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Category sx={{ fontSize: 14, mr: 0.5, color: 'primary.main' }} />
                      <Typography variant="caption" sx={{ fontWeight: 600, color: 'primary.main' }}>
                        {prompt.category_name || 'Unknown Category'}
                      </Typography>
                      <Typography variant="caption" sx={{ mx: 0.5, color: 'text.secondary' }}>
                        →
                      </Typography>
                      <Typography variant="caption" sx={{ fontWeight: 500, color: 'secondary.main' }}>
                        {prompt.sub_category_name || 'Unknown Subcategory'}
                      </Typography>
                    </Box>

                    {/* Then the prompt text */}
                    <Typography variant="body2" sx={{ fontWeight: 500, mb: 1, color: 'text.primary' }}>
                      {prompt.prompt ? prompt.prompt.substring(0, 55) + '...' : 'No content'}
                    </Typography>
                    
                    {/* Date at the bottom */}
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'flex', alignItems: 'center' }}>
                      <Schedule sx={{ fontSize: 12, mr: 0.5 }} />
                      {new Date(prompt.created_at).toLocaleDateString()}
                    </Typography>
                  </Box>
                  );
                })
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
