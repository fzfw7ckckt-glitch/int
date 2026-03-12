import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, Grid, Card, CardContent, TextField, 
  Button, Chip, Divider, List, ListItem, ListItemText,
  ListItemIcon, Paper, Stepper, Step, StepLabel, 
  IconButton, Tooltip, LinearProgress, Avatar
} from '@mui/material';
import { 
  Search as SearchIcon, 
  Add as AddIcon,
  PlayArrow as PlayIcon,
  Delete as DeleteIcon,
  History as HistoryIcon,
  AutoFixHigh as AgentIcon,
  CheckCircle as CheckCircleIcon,
  Science as LabIcon,
  DataObject as JsonIcon
} from '@mui/icons-material';
import axios from 'axios';
import Layout from '../components/Layout';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface SelectedTool {
  id: string;
  name: string;
  category: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
}

interface AvailableTool {
  id: string;
  name: string;
  category: string;
}

interface ResultItem {
  tool: string;
  data: string;
  timestamp: string;
}

export default function InvestigationHub() {
  const [query, setQuery] = useState<string>('');
  const [selectedTools, setSelectedTools] = useState<SelectedTool[]>([]);
  const [investigationStatus, setInvestigationStatus] = useState<'idle' | 'running' | 'completed'>('idle');
  const [results, setResults] = useState<ResultItem[]>([]);
  const [currentInvestigationId, setCurrentInvestigationId] = useState<string | null>(null);

  useEffect(() => {
    // Ініціалізація унікального ID для сесії розслідування
    if (typeof window !== 'undefined') {
      setCurrentInvestigationId(`inv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
    }
  }, []);

  const availableTools: AvailableTool[] = [
    { id: 'maigret', name: 'Maigret v3.0', category: 'SOCMINT' },
    { id: 'shodan', name: 'Shodan', category: 'SIGINT' },
    { id: 'geospy', name: 'GeoSpy.ai', category: 'GEOINT' },
    { id: 'pimeyes', name: 'Pimeyes', category: 'IMINT' },
  ];

  const handleAddTool = (tool: AvailableTool) => {
    if (!selectedTools.find((t: SelectedTool) => t.id === tool.id)) {
      setSelectedTools([...selectedTools, { ...tool, status: 'pending' }]);
    }
  };

  const handleRemoveTool = (id: string) => {
    setSelectedTools(selectedTools.filter((t: SelectedTool) => t.id !== id));
  };

  const handleStartInvestigation = async () => {
    if (!query || selectedTools.length === 0) return;
    
    setInvestigationStatus('running');
    const currentTools = [...selectedTools];
    setResults([]);

    for (let i = 0; i < currentTools.length; i++) {
      const tool = currentTools[i];
      tool.status = 'running';
      setSelectedTools([...currentTools]);

      try {
        // 1. Запуск задачі на бекенді
        const response = await axios.post(`${API_URL}/tools/${tool.id}/run`, {
          query: query,
          investigation_id: currentInvestigationId,
          api_key: localStorage.getItem(`api_key_${tool.id}`) || ''
        });
        
        const taskId = response.data.task_id;
        
        // 2. Полінг статусу (Long Polling симуляція)
        let ready = false;
        let attempts = 0;
        while (!ready && attempts < 30) {
          const statusRes = await axios.get(`${API_URL}/tools/status/${taskId}`);
          if (statusRes.data.ready) {
            ready = true;
            tool.status = 'completed';
            setResults((prev: ResultItem[]) => [...prev, {
              tool: tool.name,
              data: JSON.stringify(statusRes.data.result.data, null, 2),
              timestamp: new Date().toLocaleTimeString()
            }]);
          } else {
            await new Promise(resolve => setTimeout(resolve, 1000));
            attempts++;
          }
        }
      } catch (error) {
        console.error(`Error running ${tool.name}:`, error);
        tool.status = 'failed';
      }
      
      setSelectedTools([...currentTools]);
    }

    setInvestigationStatus('completed');
  };

  const handleExportSTIX = async () => {
    if (!currentInvestigationId) return;
    try {
      const response = await axios.get(`${API_URL}/vault/${currentInvestigationId}/export/stix`);
      const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `osint_stix_bundle_${currentInvestigationId}.json`;
      a.click();
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 800, mb: 1, color: '#fff' }}>
          Investigation Hub
        </Typography>
        <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.5)' }}>
          Chain multiple tools for a deep multi-vector intelligence analysis
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: 2 }}>
            <Typography variant="subtitle2" sx={{ mb: 2, color: '#fff', display: 'flex', alignItems: 'center', gap: 1 }}>
              <AgentIcon color="primary" fontSize="small" /> 1. Set Target Query
            </Typography>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Username, Email, IP or Domain..."
              value={query}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQuery(e.target.value)}
              sx={{ 
                mb: 4,
                bgcolor: 'rgba(0,0,0,0.2)',
                '& .MuiInputBase-root': { color: '#fff' },
                '& .MuiOutlinedInput-root fieldset': { borderColor: 'rgba(255,255,255,0.1)' }
              }}
            />

            <Typography variant="subtitle2" sx={{ mb: 2, color: '#fff', display: 'flex', alignItems: 'center', gap: 1 }}>
              <AddIcon color="primary" fontSize="small" /> 2. Chain OSINT Tools
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)', mb: 1, display: 'block' }}>Suggested Tools</Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {availableTools.map((tool: AvailableTool) => (
                  <Chip 
                    key={tool.id}
                    label={tool.name}
                    onClick={() => handleAddTool(tool)}
                    icon={<AddIcon />}
                    size="small"
                    sx={{ bgcolor: 'rgba(255,255,255,0.05)', color: '#fff', '&:hover': { bgcolor: 'primary.main' } }}
                  />
                ))}
              </Box>
            </Box>

            <Divider sx={{ my: 3, borderColor: 'rgba(255,255,255,0.05)' }} />

            <Typography variant="subtitle2" sx={{ mb: 2, color: '#fff' }}>Selected Pipeline</Typography>
            <List sx={{ mb: 3 }}>
              {selectedTools.length === 0 && (
                <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.3)', fontStyle: 'italic' }}>
                  No tools selected for this investigation.
                </Typography>
              )}
              {selectedTools.map((tool: SelectedTool, index: number) => (
                <ListItem 
                  key={tool.id}
                  secondaryAction={
                    <IconButton edge="end" size="small" onClick={() => handleRemoveTool(tool.id)} disabled={investigationStatus === 'running'}>
                      <DeleteIcon fontSize="small" sx={{ color: 'error.main' }} />
                    </IconButton>
                  }
                  sx={{ bgcolor: 'rgba(255,255,255,0.02)', borderRadius: 1, mb: 1 }}
                >
                  <ListItemIcon sx={{ minWidth: 30, color: 'primary.main', fontSize: '0.8rem', fontWeight: 700 }}>
                    {index + 1}
                  </ListItemIcon>
                  <ListItemText 
                    primary={tool.name} 
                    secondary={tool.category}
                    primaryTypographyProps={{ variant: 'body2', color: '#fff' }}
                    secondaryTypographyProps={{ variant: 'caption', color: 'rgba(255,255,255,0.4)' }}
                  />
                </ListItem>
              ))}
            </List>

            <Button
              fullWidth
              variant="contained"
              startIcon={<PlayIcon />}
              disabled={!query || selectedTools.length === 0 || investigationStatus === 'running'}
              onClick={handleStartInvestigation}
              sx={{ py: 1.5, fontWeight: 700 }}
            >
              Start Multi-Vector Search
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 0, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: 2, overflow: 'hidden', minHeight: '600px', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.02)', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LabIcon sx={{ color: 'primary.main' }} />
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>Investigation Pipeline</Typography>
              </Box>
              {investigationStatus === 'running' && (
                <Chip label="Processing..." size="small" color="primary" variant="outlined" />
              )}
            </Box>

            <Box sx={{ p: 3, flexGrow: 1 }}>
              {investigationStatus === 'idle' ? (
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', py: 10, opacity: 0.3 }}>
                  <SearchIcon sx={{ fontSize: 64, mb: 2 }} />
                  <Typography>Configure your investigation parameters to begin</Typography>
                </Box>
              ) : (
                <>
                  <Stepper activeStep={selectedTools.findIndex((t: SelectedTool) => t.status === 'running' || t.status === 'pending')} orientation="horizontal" sx={{ mb: 5 }}>
                    {selectedTools.map((tool: SelectedTool) => (
                      <Step key={tool.id} completed={tool.status === 'completed'}>
                        <StepLabel 
                          StepIconProps={{ sx: { color: tool.status === 'running' ? 'primary.main' : 'inherit' } }}
                        >
                          <Typography variant="caption" sx={{ color: '#fff' }}>{tool.name}</Typography>
                        </StepLabel>
                      </Step>
                    ))}
                  </Stepper>

                  <Typography variant="subtitle2" sx={{ mb: 2, color: 'primary.main', display: 'flex', alignItems: 'center', gap: 1 }}>
                    <HistoryIcon fontSize="small" /> Intelligence Stream
                  </Typography>

                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    {results.map((res: ResultItem, i: number) => (
                      <Card key={i} sx={{ bgcolor: 'rgba(0,0,0,0.2)', border: '1px solid rgba(255,255,255,0.05)' }}>
                        <CardContent sx={{ p: '16px !important' }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <CheckCircleIcon color="success" sx={{ fontSize: 16 }} />
                              <Typography variant="subtitle2" color="primary">{res.tool}</Typography>
                            </Box>
                            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.3)' }}>{res.timestamp}</Typography>
                          </Box>
                          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', fontFamily: 'monospace' }}>
                            {res.data}
                          </Typography>
                          <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                            <Button size="small" startIcon={<JsonIcon />} sx={{ fontSize: '0.6rem', color: 'rgba(255,255,255,0.5)' }}>Raw JSON</Button>
                            <Button size="small" startIcon={<AgentIcon />} sx={{ fontSize: '0.6rem', color: 'rgba(255,255,255,0.5)' }}>AI Analysis</Button>
                          </Box>
                        </CardContent>
                      </Card>
                    ))}
                    {investigationStatus === 'running' && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="caption" sx={{ color: 'primary.main', mb: 1, display: 'block' }}>
                          Executing {selectedTools.find((t: SelectedTool) => t.status === 'running')?.name}...
                        </Typography>
                        <LinearProgress />
                      </Box>
                    )}
                  </Box>
                </>
              )}
            </Box>
            
            {investigationStatus === 'completed' && (
              <Box sx={{ p: 2, bgcolor: 'rgba(76, 175, 80, 0.05)', borderTop: '1px solid rgba(76, 175, 80, 0.2)', display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                <Button variant="outlined" color="success" size="small" onClick={handleExportSTIX} startIcon={<JsonIcon />}>
                  Export STIX 2.1 (JSON)
                </Button>
                <Button variant="outlined" color="success" size="small">Export Report (PDF)</Button>
                <Button variant="contained" color="success" size="small">Save to Workspace</Button>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Layout>
  );
}
