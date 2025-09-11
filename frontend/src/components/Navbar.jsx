import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Divider,
} from '@mui/material';
import {
  AccountCircle,
  Dashboard,
  History,
  AdminPanelSettings,
  Logout,
  School,
  ExpandMore,
  Menu as MenuIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();
  const { user, logout, isAuthenticated, isAdmin } = useAuth();

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    handleClose();
  };

  const handleNavigation = (path) => {
    navigate(path);
    handleClose();
  };

  return (
    <AppBar position="static" elevation={2}>
      <Toolbar>
        <School sx={{ mr: 2 }} />
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, fontWeight: 600 }}
        >
          AI Learning Platform
        </Typography>

        {isAuthenticated() ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            {/* Quick Navigation Buttons for larger screens */}
            <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
              <Button 
                size="small" 
                color="inherit" 
                onClick={() => navigate('/dashboard')}
                startIcon={<Dashboard />}
                sx={{ textTransform: 'none' }}
              >
                Dashboard
              </Button>
              <Button 
                size="small" 
                color="inherit" 
                onClick={() => navigate('/history')}
                startIcon={<History />}
                sx={{ textTransform: 'none' }}
              >
                History
              </Button>
              {isAdmin() && (
                <Button 
                  size="small" 
                  color="inherit" 
                  onClick={() => navigate('/admin')}
                  startIcon={<AdminPanelSettings />}
                  sx={{ textTransform: 'none' }}
                >
                  Admin
                </Button>
              )}
            </Box>

            {/* Profile section with avatar */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Avatar sx={{ width: 32, height: 32, bgcolor: 'rgba(255,255,255,0.2)' }}>
                <AccountCircle />
              </Avatar>
              <Typography variant="body2" sx={{ color: 'white', opacity: 0.9, display: { xs: 'none', sm: 'block' } }}>
                Welcome, {user?.name || user?.email}
              </Typography>
            </Box>
            
            {/* Mobile Menu Button */}
            <IconButton
              size="small"
              aria-label="mobile menu"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              color="inherit"
              sx={{ 
                display: { xs: 'block', md: 'none' },
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.1)',
                },
              }}
            >
              <MenuIcon />
            </IconButton>

            {/* Logout Button */}
            <Button
              size="small"
              color="inherit"
              onClick={handleLogout}
              startIcon={<Logout />}
              sx={{ 
                textTransform: 'none',
                display: { xs: 'none', md: 'flex' },
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.1)',
                },
              }}
            >
              Logout
            </Button>
            
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
              sx={{ display: { xs: 'block', md: 'none' } }} // Only show on mobile
              PaperProps={{
                elevation: 8,
                sx: {
                  minWidth: 200,
                  mt: 1,
                  borderRadius: 2,
                  '& .MuiMenuItem-root': {
                    px: 2,
                    py: 1.5,
                    borderRadius: 1,
                    mx: 1,
                    my: 0.5,
                    '&:hover': {
                      bgcolor: 'primary.50',
                    },
                  },
                },
              }}
            >
              {/* Mobile Menu - Simplified */}
              <MenuItem onClick={() => handleNavigation('/dashboard')} sx={{ fontWeight: 500 }}>
                <Dashboard sx={{ mr: 1, color: 'primary.main' }} />
                Dashboard
              </MenuItem>
              <MenuItem onClick={() => handleNavigation('/history')} sx={{ fontWeight: 500 }}>
                <History sx={{ mr: 1, color: 'secondary.main' }} />
                Learning History
              </MenuItem>
              {isAdmin() && (
                <MenuItem onClick={() => handleNavigation('/admin')} sx={{ fontWeight: 500 }}>
                  <AdminPanelSettings sx={{ mr: 1, color: 'warning.main' }} />
                  Admin Panel
                </MenuItem>
              )}
              <Divider sx={{ my: 1 }} />
              <MenuItem onClick={handleLogout} sx={{ fontWeight: 500, color: 'error.main' }}>
                <Logout sx={{ mr: 1 }} />
                Logout
              </MenuItem>
            </Menu>
          </Box>
        ) : (
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button 
              color="inherit" 
              onClick={() => navigate('/login')}
              sx={{ textTransform: 'none' }}
            >
              Login
            </Button>
            <Button 
              color="inherit" 
              onClick={() => navigate('/register')}
              sx={{ textTransform: 'none' }}
            >
              Register
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
