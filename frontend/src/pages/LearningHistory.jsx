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
  const itemsPerPage = 6;

  useEffect(() => {
    loadPrompts();
  }, []);

  useEffect(() => {
    filterPrompts();
  }, [prompts, searchTerm]);

  const loadPrompts = async () => {
    try {
      setLoading(true);
      const response = await promptsAPI.getUserPrompts();
      setPrompts(response.data);
    } catch (error) {
      setError('Failed to load learning history');
    } finally {
      setLoading(false);
    }
  };

  const filterPrompts = () => {
    if (!searchTerm.trim()) {
      setFilteredPrompts(prompts);
    } else {
      const filtered = prompts.filter(prompt =>
        prompt.prompt_text.toLowerCase().includes(searchTerm.toLowerCase()) ||
        prompt.category?.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        prompt.sub_category?.name.toLowerCase().includes(searchTerm.toLowerCase())
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
            Learning History
          </Typography>
        </Box>
        <Typography variant="h6" color="text.secondary">
          Review your AI-generated lessons and track your learning progress
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Search and Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <TextField
            fullWidth
            placeholder="Search your lessons..."
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
          <Grid container spacing={3}>
            {paginatedPrompts.map((prompt) => (
              <Grid item xs={12} key={prompt.id}>
                <Card elevation={2} sx={{ '&:hover': { elevation: 4 } }}>
                  <CardContent>
                    <Grid container spacing={2}>
                      <Grid item xs={12} md={8}>
                        <Box sx={{ display: 'flex', alignItems: 'start', gap: 2, mb: 2 }}>
                          <AutoAwesome sx={{ color: 'primary.main', mt: 0.5 }} />
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="h6" sx={{ fontWeight: 500, mb: 1 }}>
                              {prompt.prompt_text}
                            </Typography>
                            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                              <Chip
                                icon={<Category />}
                                label={prompt.category?.name}
                                color="primary"
                                variant="outlined"
                                size="small"
                              />
                              <Chip
                                label={prompt.sub_category?.name}
                                color="secondary"
                                variant="outlined"
                                size="small"
                              />
                            </Box>
                          </Box>
                        </Box>
                      </Grid>
                      
                      <Grid item xs={12} md={4}>
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <CalendarToday sx={{ fontSize: 16, color: 'text.secondary' }} />
                            <Typography variant="body2" color="text.secondary">
                              {formatDate(prompt.created_at)}
                            </Typography>
                          </Box>
                          <IconButton
                            onClick={() => handleExpandPrompt(prompt.id)}
                            sx={{ ml: 1 }}
                          >
                            {expandedPrompt === prompt.id ? <ExpandLess /> : <ExpandMore />}
                          </IconButton>
                        </Box>
                      </Grid>
                    </Grid>

                    <Collapse in={expandedPrompt === prompt.id} timeout="auto" unmountOnExit>
                      <Box sx={{ mt: 2 }}>
                        <LessonDisplay 
                          content={prompt.ai_response} 
                          title="Historical Lesson"
                        />
                      </Box>
                    </Collapse>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

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
    </Container>
  );
};

export default LearningHistory;
