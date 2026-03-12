import React, { useState, useEffect } from 'react';
import { 
  Box, Drawer, List, ListItem, ListItemIcon, ListItemText, 
  AppBar, Toolbar, Typography, Divider, IconButton, Badge,
  Tooltip, Avatar, useTheme, alpha
} from '@mui/material';
import { 
  Dashboard as DashboardIcon, 
  Search as SearchIcon, 
  Security as SecurityIcon, 
  Map as MapIcon, 
  Assessment as AssessmentIcon,
  Settings as SettingsIcon,
  Notifications as NotificationsIcon,
  Menu as MenuIcon,
  TravelExplore as OSINTIcon,
  Terminal as TerminalIcon,
  History as HistoryIcon,
  AccountTree as GraphIcon
} from '@mui/icons-material';
import Link from 'next/link';
import { useRouter } from 'next/router';

const drawerWidth = 260;

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const theme = useTheme();
  const router = useRouter();
  const [mobileOpen, setMobileOpen] = useState(false);

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
    { text: 'Investigation Hub', icon: <SearchIcon />, path: '/investigation' },
    { text: 'Tools Catalog', icon: <OSINTIcon />, path: '/tools' },
    { text: 'Visual Graph', icon: <GraphIcon />, path: '/graph' },
    { text: 'Terminal', icon: <TerminalIcon />, path: '/terminal' },
    { text: 'History', icon: <HistoryIcon />, path: '/history' },
  ];

  const secondaryItems = [
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
    { text: 'Security', icon: <SecurityIcon />, path: '/security' },
  ];

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', bgcolor: '#0a0c10', color: '#fff' }}>
      <Box sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Avatar sx={{ bgcolor: theme.palette.primary.main, width: 40, height: 40 }}>
          <OSINTIcon />
        </Avatar>
        <Typography variant="h6" sx={{ fontWeight: 800, letterSpacing: 1, color: '#fff' }}>
          MINIMAX <span style={{ color: theme.palette.primary.main }}>OSINT</span>
        </Typography>
      </Box>
      
      <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)' }} />
      
      <List sx={{ px: 2, py: 3, flexGrow: 1 }}>
        {menuItems.map((item) => {
          const isActive = router.pathname === item.path;
          return (
            <Link href={item.path} key={item.text} style={{ textDecoration: 'none', color: 'inherit' }}>
              <ListItem 
                button 
                sx={{ 
                  borderRadius: 2,
                  mb: 1,
                  bgcolor: isActive ? 'rgba(33, 150, 243, 0.15)' : 'transparent',
                  color: isActive ? theme.palette.primary.main : 'rgba(255,255,255,0.7)',
                  '&:hover': {
                    bgcolor: 'rgba(255,255,255,0.05)',
                    color: '#fff'
                  }
                }}
              >
                <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} primaryTypographyProps={{ variant: 'body2', fontWeight: isActive ? 600 : 400 }} />
              </ListItem>
            </Link>
          );
        })}
      </List>

      <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)' }} />

      <List sx={{ px: 2, py: 2 }}>
        {secondaryItems.map((item) => (
          <Link href={item.path} key={item.text} style={{ textDecoration: 'none', color: 'inherit' }}>
            <ListItem 
              button 
              sx={{ 
                borderRadius: 2,
                mb: 0.5,
                color: 'rgba(255,255,255,0.5)',
                '&:hover': { bgcolor: 'rgba(255,255,255,0.05)', color: '#fff' }
              }}
            >
              <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} primaryTypographyProps={{ variant: 'body2' }} />
            </ListItem>
          </Link>
        ))}
      </List>
      
      <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.03)', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          <Badge color="success" variant="dot" overlap="circular">
            <Avatar sx={{ width: 32, height: 32 }}>U</Avatar>
          </Badge>
          <Box>
            <Typography variant="caption" sx={{ display: 'block', fontWeight: 600 }}>Administrator</Typography>
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)' }}>Online • API Secure</Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#0f1117' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          bgcolor: 'rgba(15, 17, 23, 0.8)',
          backdropFilter: 'blur(8px)',
          boxShadow: 'none',
          borderBottom: '1px solid rgba(255,255,255,0.05)',
        }}
      >
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="subtitle2" sx={{ color: 'rgba(255,255,255,0.5)', fontWeight: 400 }}>
              {router.pathname.split('/').filter(x => x).map(x => x.charAt(0).toUpperCase() + x.slice(1)).join(' / ') || 'Dashboard'}
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Tooltip title="Notifications">
              <IconButton color="inherit" size="small">
                <Badge badgeContent={4} color="error">
                  <NotificationsIcon fontSize="small" />
                </Badge>
              </IconButton>
            </Tooltip>
            <Tooltip title="Quick Search">
              <IconButton color="inherit" size="small">
                <SearchIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </AppBar>

      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, borderRight: 'none' },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, borderRight: '1px solid rgba(255,255,255,0.05)' },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: '64px',
        }}
      >
        {children}
      </Box>
    </Box>
  );
}
