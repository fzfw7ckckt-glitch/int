import React, { useState, useEffect } from 'react';
import { 
  Container, Typography, Grid, Card, CardContent, Chip, Box, 
  TextField, InputAdornment, Button, Menu, MenuItem, 
  Dialog, DialogTitle, DialogContent, DialogActions,
  IconButton, Tooltip, Alert, Snackbar, Skeleton, Divider
} from '@mui/material';
import { 
  Search as SearchIcon, 
  FilterList as FilterIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  VpnKey as KeyIcon,
  Launch as LaunchIcon,
  PlayArrow as PlayIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import axios from 'axios';
import Layout from '../components/Layout';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Tool {
  id: string;
  name: string;
  category: string;
  description: string;
  type: string;
  api: string;
}

interface CategoryData {
  name: string;
  count: number;
  tools: Tool[];
}

export default function ToolsPage() {
  const [categories, setCategories] = useState<{ [key: string]: CategoryData }>({});
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  
  // Tool Detail Modal
  const [selectedTool, setSelectedTool] = useState<Tool | null>(null);
  const [apiKey, setApiKey] = useState('');
  const [runQuery, setRunQuery] = useState('');
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' as 'info' | 'success' | 'error' });

  useEffect(() => {
    fetchTools();
  }, []);

  const fetchTools = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/tools/`);
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Failed to fetch tools:', error);
      showSnackbar('Failed to load tools catalog', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showSnackbar = (message: string, severity: 'info' | 'success' | 'error' = 'info') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value.toLowerCase());
  };

  const handleFilterClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleFilterClose = (category: string | null) => {
    setSelectedCategory(category);
    setAnchorEl(null);
  };

  const handleToolClick = (tool: Tool) => {
    setSelectedTool(tool);
    setApiKey(localStorage.getItem(`api_key_${tool.id}`) || '');
  };

  const handleSaveKey = () => {
    if (selectedTool) {
      // Маскування ключа перед збереженням (візуальне)
      const maskedKey = apiKey.length > 8 
        ? `${apiKey.substring(0, 4)}****${apiKey.substring(apiKey.length - 4)}`
        : '****';
      
      localStorage.setItem(`api_key_${selectedTool.id}`, apiKey);
      showSnackbar(`API Key for ${selectedTool.name} saved locally (${maskedKey})`, 'success');
    }
  };

  const handleRunTool = async () => {
    if (!selectedTool) return;
    
    try {
      showSnackbar(`Initializing ${selectedTool.name}...`, 'info');
      const response = await axios.post(`${API_URL}/tools/${selectedTool.id}/run`, {
        query: runQuery,
        api_key: apiKey
      });
      showSnackbar(`Task started: ${response.data.task_id}`, 'success');
    } catch (error) {
      showSnackbar('Failed to run tool', 'error');
    }
  };

  const filteredTools = Object.entries(categories).flatMap(([catKey, catData]) => 
    catData.tools.filter(tool => {
      const matchesSearch = tool.name.toLowerCase().includes(searchQuery) || 
                           tool.description.toLowerCase().includes(searchQuery);
      const matchesCategory = !selectedCategory || catKey === selectedCategory;
      return matchesSearch && matchesCategory;
    })
  );

  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 800, mb: 1, color: '#fff' }}>
          Tools Catalog
        </Typography>
        <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.5)' }}>
          Explore and manage 150+ integrated OSINT intelligence tools
        </Typography>
      </Box>

      <Box sx={{ mb: 4, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Search by tool name, description or capability..."
          value={searchQuery}
          onChange={handleSearch}
          sx={{ 
            flexGrow: 1,
            bgcolor: 'rgba(255,255,255,0.03)',
            '& .MuiOutlinedInput-root': {
              color: '#fff',
              '& fieldset': { borderColor: 'rgba(255,255,255,0.1)' },
              '&:hover fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
            }
          }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon sx={{ color: 'rgba(255,255,255,0.3)' }} />
              </InputAdornment>
            ),
          }}
        />
        <Button
          variant="outlined"
          startIcon={<FilterIcon />}
          onClick={handleFilterClick}
          sx={{ borderColor: 'rgba(255,255,255,0.1)', color: '#fff' }}
        >
          {selectedCategory ? categories[selectedCategory]?.name : 'All Categories'}
        </Button>
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={() => handleFilterClose(selectedCategory)}
          PaperProps={{
            sx: { bgcolor: '#1a1d24', color: '#fff', border: '1px solid rgba(255,255,255,0.1)' }
          }}
        >
          <MenuItem onClick={() => handleFilterClose(null)}>All Categories</MenuItem>
          <Divider sx={{ borderColor: 'rgba(255,255,255,0.05)' }} />
          {Object.entries(categories).map(([key, cat]) => (
            <MenuItem key={key} onClick={() => handleFilterClose(key)}>
              {cat.name} ({cat.count})
            </MenuItem>
          ))}
        </Menu>
      </Box>

      {loading ? (
        <Grid container spacing={2}>
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Grid item xs={12} sm={6} md={4} key={i}>
              <Skeleton variant="rectangular" height={160} sx={{ borderRadius: 2, bgcolor: 'rgba(255,255,255,0.05)' }} />
            </Grid>
          ))}
        </Grid>
      ) : (
        <Grid container spacing={2}>
          {filteredTools.map((tool) => (
            <Grid item xs={12} sm={6} md={4} key={tool.id}>
              <Card 
                onClick={() => handleToolClick(tool)}
                sx={{ 
                  height: '100%', 
                  bgcolor: 'rgba(255,255,255,0.03)', 
                  border: '1px solid rgba(255,255,255,0.05)',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  '&:hover': {
                    bgcolor: 'rgba(255,255,255,0.06)',
                    transform: 'translateY(-4px)',
                    borderColor: 'primary.main'
                  }
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="h6" sx={{ color: '#fff', fontWeight: 600 }}>{tool.name}</Typography>
                    <Box sx={{ display: 'flex', gap: 0.5 }}>
                      {tool.api === '✓' ? (
                        <Tooltip title="API Support Available">
                          <CheckCircleIcon sx={{ color: 'success.main', fontSize: 18 }} />
                        </Tooltip>
                      ) : (
                        <Tooltip title="Direct Web Only">
                          <CancelIcon sx={{ color: 'rgba(255,255,255,0.2)', fontSize: 18 }} />
                        </Tooltip>
                      )}
                    </Box>
                  </Box>
                  
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)', mb: 2, height: 40, overflow: 'hidden' }}>
                    {tool.description}
                  </Typography>

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Chip 
                      label={tool.type} 
                      size="small" 
                      sx={{ bgcolor: 'rgba(255,255,255,0.05)', color: 'rgba(255,255,255,0.6)', fontSize: '0.7rem' }} 
                    />
                    <Typography variant="caption" sx={{ color: 'primary.main' }}>Details →</Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Tool Details & API Config Dialog */}
      <Dialog 
        open={Boolean(selectedTool)} 
        onClose={() => setSelectedTool(null)}
        maxWidth="sm"
        fullWidth
        PaperProps={{
          sx: { bgcolor: '#1a1d24', color: '#fff', border: '1px solid rgba(255,255,255,0.1)' }
        }}
      >
        {selectedTool && (
          <>
            <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Typography variant="h5" sx={{ fontWeight: 700 }}>{selectedTool.name}</Typography>
                <Chip label={selectedTool.category} size="small" color="primary" />
              </Box>
              <IconButton onClick={() => setSelectedTool(null)} sx={{ color: 'rgba(255,255,255,0.5)' }}>
                <CancelIcon />
              </IconButton>
            </DialogTitle>
            <DialogContent dividers sx={{ borderColor: 'rgba(255,255,255,0.05)' }}>
              <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.7)', mb: 3 }}>
                {selectedTool.description}
              </Typography>

              {selectedTool.api === '✓' ? (
                <Box sx={{ bgcolor: 'rgba(33, 150, 243, 0.05)', p: 2, borderRadius: 2, border: '1px solid rgba(33, 150, 243, 0.2)', mb: 3 }}>
                  <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1, color: 'primary.main' }}>
                    <KeyIcon fontSize="small" /> API Configuration
                  </Typography>
                  <Typography variant="caption" sx={{ display: 'block', mb: 2, color: 'rgba(255,255,255,0.5)' }}>
                    Your API key is stored locally in your browser for security.
                  </Typography>
                  <TextField
                    fullWidth
                    size="small"
                    type="password"
                    label="API Key / Token"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    sx={{ 
                      '& .MuiInputBase-root': { color: '#fff' },
                      '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.5)' },
                      '& .MuiOutlinedInput-root fieldset': { borderColor: 'rgba(255,255,255,0.1)' }
                    }}
                  />
                  <Button 
                    size="small" 
                    variant="contained" 
                    onClick={handleSaveKey}
                    sx={{ mt: 1 }}
                  >
                    Save Key Locally
                  </Button>
                </Box>
              ) : (
                <Alert severity="info" sx={{ mb: 3, bgcolor: 'rgba(2, 136, 209, 0.1)', color: '#fff' }}>
                  This tool does not support direct API integration. Click "Open Website" to use it manually.
                </Alert>
              )}

              <Typography variant="subtitle2" sx={{ mb: 1, color: '#fff' }}>Quick Run (MiniMax Agent)</Typography>
              <TextField
                fullWidth
                multiline
                rows={2}
                placeholder="Enter target (domain, email, username)..."
                value={runQuery}
                onChange={(e) => setRunQuery(e.target.value)}
                sx={{ 
                  bgcolor: 'rgba(255,255,255,0.03)',
                  '& .MuiInputBase-root': { color: '#fff' },
                  '& .MuiOutlinedInput-root fieldset': { borderColor: 'rgba(255,255,255,0.1)' }
                }}
              />
            </DialogContent>
            <DialogActions sx={{ p: 2, bgcolor: 'rgba(0,0,0,0.2)' }}>
              <Button 
                startIcon={<LaunchIcon />}
                sx={{ color: 'rgba(255,255,255,0.6)' }}
                onClick={() => window.open(`https://www.google.com/search?q=${selectedTool.name}+osint`, '_blank')}
              >
                Open Website
              </Button>
              <Box sx={{ flexGrow: 1 }} />
              <Button onClick={() => setSelectedTool(null)} sx={{ color: 'rgba(255,255,255,0.5)' }}>Cancel</Button>
              <Button 
                variant="contained" 
                startIcon={<PlayIcon />}
                disabled={selectedTool.api !== '✓'}
                onClick={handleRunTool}
              >
                Execute Tool
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity} variant="filled" sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Layout>
  );
}
