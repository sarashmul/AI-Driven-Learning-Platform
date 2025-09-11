import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Divider,
  Chip,
} from '@mui/material';
import {
  AutoAwesome,
} from '@mui/icons-material';
import './LessonDisplay.css';

const LessonDisplay = ({ content, title = "Your Generated Lesson" }) => {
  
  // Function to render content with proper formatting
  const renderFormattedContent = (text) => {
    if (!text) return null;

    // Split content by lines
    const lines = text.split('\n');
    const elements = [];
    let currentCodeBlock = '';
    let isInCodeBlock = false;

    lines.forEach((line, index) => {
      const trimmedLine = line.trim();

      // Handle code blocks
      if (trimmedLine.startsWith('```')) {
        if (isInCodeBlock) {
          // End of code block
          if (currentCodeBlock.trim()) {
            elements.push(
              <Paper
                key={`code-${index}`}
                sx={{
                  p: 2,
                  mb: 2,
                  backgroundColor: '#f5f5f5',
                  border: '1px solid #e0e0e0',
                  borderRadius: 1,
                  fontFamily: 'monospace',
                  overflow: 'auto'
                }}
              >
                <Typography
                  component="pre"
                  sx={{
                    fontFamily: 'monospace',
                    fontSize: '0.9rem',
                    margin: 0,
                    whiteSpace: 'pre-wrap',
                    color: '#333'
                  }}
                >
                  {currentCodeBlock}
                </Typography>
              </Paper>
            );
          }
          currentCodeBlock = '';
          isInCodeBlock = false;
        } else {
          // Start of code block
          isInCodeBlock = true;
        }
        return;
      }

      if (isInCodeBlock) {
        currentCodeBlock += line + '\n';
        return;
      }

      // Handle headers (markdown style with # symbols)
      if (trimmedLine.startsWith('#')) {
        const headerLevel = trimmedLine.match(/^#+/)[0].length;
        const headerText = trimmedLine.replace(/^#+\s*/, '');
        
        // Different styles for different header levels
        let headerVariant = 'h4';
        let headerSx = {
          fontWeight: 700,
          color: 'primary.main',
          mt: 3,
          mb: 1.5,
          borderBottom: '2px solid',
          borderColor: 'primary.main',
          pb: 0.5
        };

        switch (headerLevel) {
          case 1: // # Main Title
            headerVariant = 'h3';
            headerSx = {
              ...headerSx,
              fontSize: '2rem',
              borderBottom: '3px solid',
              borderColor: 'primary.dark',
              color: 'primary.dark',
              mt: 4,
              mb: 2
            };
            break;
          case 2: // ## Subtitle
            headerVariant = 'h4';
            headerSx = {
              ...headerSx,
              fontSize: '1.5rem',
              borderBottom: '2px solid',
              borderColor: 'primary.main',
              color: 'primary.main'
            };
            break;
          case 3: // ### Section
            headerVariant = 'h5';
            headerSx = {
              ...headerSx,
              fontSize: '1.25rem',
              borderBottom: '1px solid',
              borderColor: 'secondary.main',
              color: 'secondary.main'
            };
            break;
          default: // #### and more
            headerVariant = 'h6';
            headerSx = {
              ...headerSx,
              fontSize: '1.1rem',
              borderBottom: 'none',
              borderLeft: '4px solid',
              borderColor: 'info.main',
              color: 'info.main',
              pl: 2
            };
        }

        elements.push(
          <Typography
            key={`header-${index}`}
            variant={headerVariant}
            sx={headerSx}
          >
            {headerText}
          </Typography>
        );
      }
      // Handle other headers (lines that are short and likely titles - backup detection)
      else if (
        trimmedLine.length > 0 &&
        trimmedLine.length < 100 &&
        !trimmedLine.includes('.') &&
        (trimmedLine.match(/^[A-Z]/) || trimmedLine.includes(':')) &&
        !trimmedLine.startsWith('-') &&
        !trimmedLine.startsWith('•') &&
        !trimmedLine.startsWith('`')
      ) {
        elements.push(
          <Typography
            key={`fallback-header-${index}`}
            variant="h6"
            sx={{
              fontWeight: 600,
              color: 'text.primary',
              mt: 2,
              mb: 1,
              borderLeft: '3px solid',
              borderColor: 'warning.main',
              pl: 1.5,
              backgroundColor: 'warning.50'
            }}
          >
            {trimmedLine.replace(/^#+\s*/, '').replace(/:$/, '')}
          </Typography>
        );
      }
      // Handle bullet points
      else if (trimmedLine.startsWith('-') || trimmedLine.startsWith('•')) {
        elements.push(
          <Typography
            key={`bullet-${index}`}
            variant="body1"
            sx={{
              ml: 2,
              mb: 0.5,
              display: 'flex',
              alignItems: 'flex-start'
            }}
          >
            <span style={{ marginRight: '8px', color: '#1976d2' }}>•</span>
            {trimmedLine.replace(/^[-•]\s*/, '')}
          </Typography>
        );
      }
      // Handle regular paragraphs
      else if (trimmedLine.length > 0) {
        elements.push(
          <Typography
            key={`text-${index}`}
            variant="body1"
            paragraph
            sx={{
              lineHeight: 1.8,
              textAlign: 'justify',
              mb: 1.5
            }}
          >
            {trimmedLine}
          </Typography>
        );
      }
      // Handle empty lines (add spacing)
      else {
        elements.push(<Box key={`space-${index}`} sx={{ height: '8px' }} />);
      }
    });

    return elements;
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Divider sx={{ mb: 4 }} />
      
      {/* Header */}
      <Paper
        elevation={3}
        sx={{
          background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
          color: 'white',
          p: 3,
          mb: 4,
          borderRadius: 2
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <AutoAwesome sx={{ mr: 2, fontSize: 32 }} />
            <Typography variant="h4" sx={{ fontWeight: 600 }}>
              {title}
            </Typography>
          </Box>
          <Chip 
            label="✨ AI Generated"
            sx={{ 
              backgroundColor: 'rgba(255,255,255,0.2)',
              color: 'white',
              fontWeight: 600,
              fontSize: '0.875rem'
            }}
          />
        </Box>
      </Paper>

      {/* Content */}
      <Paper
        elevation={2}
        sx={{
          p: 4,
          backgroundColor: 'white',
          borderRadius: 2,
          border: '1px solid #e0e0e0'
        }}
      >
        {renderFormattedContent(content)}
      </Paper>

      {/* Footer */}
      <Box
        sx={{
          mt: 3,
          p: 2,
          backgroundColor: 'success.50',
          borderRadius: 2,
          textAlign: 'center',
          border: '1px solid #c8e6c9'
        }}
      >
        <Typography variant="body1" sx={{ fontWeight: 500, color: 'success.dark' }}>
          🎓 Continue exploring and learning new topics!
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
          This comprehensive lesson was generated by AI to accelerate your learning
        </Typography>
      </Box>
    </Box>
  );
};

export default LessonDisplay;
