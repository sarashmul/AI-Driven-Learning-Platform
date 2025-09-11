import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Box,
  Grid,
  Chip,
  TextField,
  InputAdornment,
  Pagination,
  Alert,
  Paper,
  Divider,
  IconButton,
  Collapse,
} from '@mui/material';
import {
  History,
  Search,
  ExpandMore,
  ExpandLess,
  AutoAwesome,
  CalendarToday,
  Category,
  Schedule,
} from '@mui/icons-material';
import { promptsAPI } from '../services/api';
import LessonDisplay from '../components/LessonDisplay';

const LearningHistory = () => {
  const [prompts, setPrompts] = useState([]);
  const [filteredPrompts, setFilteredPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [expandedPrompt, setExpandedPrompt] = useState(null);
  const [selectedHistoricalLesson, setSelectedHistoricalLesson] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminStats, setAdminStats] = useState(null);
  const itemsPerPage = 3;

  useEffect(() => {
    loadPrompts();
    checkAdminStatus();
  }, []);

  const checkAdminStatus = () => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const isUserAdmin = user.role === 'admin';
    setIsAdmin(isUserAdmin);
    
    if (isUserAdmin) {
      loadAdminStats();
    }
  };

  const loadAdminStats = async () => {
    try {
      const response = await promptsAPI.getAdminStats();
      setAdminStats(response.data);
    } catch (error) {
      console.error('Failed to load admin stats:', error);
    }
  };

  const loadPrompts = async () => {
    try {
      setLoading(true);
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      
      let response;
      if (user.role === 'admin') {
        response = await promptsAPI.getAllPromptsAdmin();
      } else {
        response = await promptsAPI.getUserPrompts();
      }
      
      setPrompts(response.data);
    } catch (error) {
      setError('Failed to load learning history');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    filterPrompts();
  }, [prompts, searchTerm]);

  const filterPrompts = () => {
    if (!searchTerm.trim()) {
      setFilteredPrompts(prompts);
    } else {
      const filtered = prompts.filter(prompt =>
        prompt.prompt.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (prompt.category_name && prompt.category_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (prompt.sub_category_name && prompt.sub_category_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (isAdmin && prompt.user_name && prompt.user_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (isAdmin && prompt.user_email && prompt.user_email.toLowerCase().includes(searchTerm.toLowerCase()))
      );
      setFilteredPrompts(filtered);
    }
    setPage(1); // Reset to first page when filtering
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
    setExpandedPrompt(null); // Collapse any expanded prompt when changing pages
  };

  const handleExpandPrompt = (promptId) => {
    setExpandedPrompt(expandedPrompt === promptId ? null : promptId);
  };

  const handleHistoricalLessonClick = (prompt) => {
    setSelectedHistoricalLesson(prompt.response);
    setExpandedPrompt(null); // Close any expanded prompt
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const paginatedPrompts = filteredPrompts.slice(
    (page - 1) * itemsPerPage,
    page * itemsPerPage
  );

  const totalPages = Math.ceil(filteredPrompts.length / itemsPerPage);

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
          <Typography>Loading your learning history...</Typography>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <History sx={{ mr: 2, color: 'primary.main', fontSize: 32 }} />
          <Typography variant="h3" component="h1" sx={{ fontWeight: 600 }}>
            {isAdmin ? 'All Users Learning History (Admin)' : 'Learning History'}
          </Typography>
        </Box>
        <Typography variant="h6" color="text.secondary">
          {isAdmin 
            ? 'View and manage all users\' AI-generated lessons and learning progress'
            : 'Review your AI-generated lessons and track your learning progress'
          }
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Search and Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={isAdmin ? 6 : 8}>
          <TextField
            fullWidth
            placeholder={isAdmin ? "Search lessons by content, category, or user..." : "Search your lessons..."}
            value={searchTerm}
            onChange={handleSearchChange}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
            sx={{ backgroundColor: 'white' }}
          />
        </Grid>
        
        {isAdmin && adminStats ? (
          <>
            <Grid item xs={6} md={2}>
              <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h4" color="primary.main" sx={{ fontWeight: 600 }}>
                  {adminStats.total_prompts}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Lessons
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={6} md={2}>
              <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h4" color="secondary.main" sx={{ fontWeight: 600 }}>
                  {adminStats.total_users}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Users
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={6} md={2}>
              <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h4" color="success.main" sx={{ fontWeight: 600 }}>
                  {adminStats.total_categories}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Categories
                </Typography>
              </Paper>
            </Grid>
          </>
        ) : (
          <Grid item xs={12} md={4}>
            <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary.main" sx={{ fontWeight: 600 }}>
                {prompts.length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Lessons Generated
              </Typography>
            </Paper>
          </Grid>
        )}
      </Grid>

      {/* Learning History Cards */}
      {filteredPrompts.length === 0 ? (
        <Paper elevation={1} sx={{ p: 4, textAlign: 'center' }}>
          <AutoAwesome sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            {searchTerm ? 'No lessons found matching your search' : 'No lessons generated yet'}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {searchTerm ? 'Try different search terms' : 'Start learning by generating your first lesson!'}
          </Typography>
        </Paper>
      ) : (
        <>
          <Box sx={{ maxWidth: '800px', mx: 'auto' }}>
            {paginatedPrompts.map((prompt) => (
              <Box 
                key={prompt.id}
                sx={{ 
                  mb: 2,
                  p: 3,
                  border: '1px solid #e0e0e0',
                  borderRadius: 2,
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  backgroundColor: 'white',
                  '&:hover': {
                    backgroundColor: 'primary.50',
                    borderColor: 'primary.main',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 4px 12px rgba(25, 118, 210, 0.15)'
                  }
                }}
                onClick={() => handleHistoricalLessonClick(prompt)}
              >
                  {/* User info for admin */}
                  {isAdmin && (
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1, p: 1, backgroundColor: 'grey.50', borderRadius: 1 }}>
                      <Typography variant="caption" sx={{ fontWeight: 600, color: 'info.main', mr: 1 }}>
                        User:
                      </Typography>
                      <Typography variant="caption" sx={{ fontWeight: 500, color: 'text.primary' }}>
                        {prompt.user_name} ({prompt.user_email})
                      </Typography>
                    </Box>
                  )}

                  {/* Category and Subcategory */}
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
                  <Typography variant="body2" sx={{ fontWeight: 500, mb: 2, color: 'text.primary', fontSize: '0.95rem' }}>
                    {prompt.prompt ? prompt.prompt.substring(0, 100) + '...' : 'No content'}
                  </Typography>
                  
                  {/* Date at the bottom */}
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'flex', alignItems: 'center' }}>
                    <Schedule sx={{ fontSize: 12, mr: 0.5 }} />
                    {new Date(prompt.created_at).toLocaleDateString()}
                  </Typography>
                </Box>
            ))}
          </Box>

          {/* Pagination */}
          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="primary"
                size="large"
                showFirstButton
                showLastButton
              />
            </Box>
          )}
        </>
      )}

      {/* Display selected historical lesson */}
      {selectedHistoricalLesson && (
        <Box sx={{ mt: 4 }}>
          <LessonDisplay 
            content={selectedHistoricalLesson} 
            title="Historical Lesson"
          />
        </Box>
      )}
    </Container>
  );
};

export default LearningHistory;
