import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid, Card, CardContent, Button, Box } from '@mui/material';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [status, setStatus] = useState('checking');
  const [stats, setStats] = useState({ tools: 0, categories: 0 });

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await axios.get(`${API_URL}/health/`);
        setStatus('online');
        
        const toolsResponse = await axios.get(`${API_URL}/tools/`);
        setStats({ 
          tools: toolsResponse.data.total_tools || 150,
          categories: toolsResponse.data.total_categories || 16
        });
      } catch (error) {
        setStatus('offline');
      }
    };

    checkHealth();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          🛡️ OSINT Platform 2026
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Hybrid intelligence gathering with 50+ integrated tools
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Service Status
              </Typography>
              <Typography variant="h5">
                {status === 'online' ? '✅ Online' : '❌ Offline'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Available Tools
              </Typography>
              <Typography variant="h5">
                {stats.tools}+
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Categories
              </Typography>
              <Typography variant="h5">
                {stats.categories || 16}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Users
              </Typography>
              <Typography variant="h5">
                Loading...
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Button variant="contained" color="primary" size="large">
          Start Investigation
        </Button>
        <Button variant="outlined" color="primary" size="large" sx={{ ml: 2 }}>
          Browse Tools
        </Button>
      </Box>
    </Container>
  );
}
