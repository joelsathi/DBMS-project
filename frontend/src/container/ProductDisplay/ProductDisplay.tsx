import * as React from 'react';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import TopBar from './TopBar';
import Products from './Products';


function Copyright(props: any) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      {/* TODO update this link to your own website */}
      <Link color="inherit" href="https://mui.com/"> 
        thulasiStores
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const mdTheme = createTheme({
  palette: {
    primary: {
      main: '#9fa8da',
    },
    secondary: {
      main: '#212121',
    },
  },
  components: {
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: "#9fa8da",
          color: "black",
        }
      }

    }
  },
});

function DashboardContent() {
  const [open, setOpen] = React.useState(true);
  const toggleDrawer = () => {
    setOpen(!open);
  };

  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <TopBar />

        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Toolbar />
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
               <Grid item xs={2} sm={4} md={4} > 
                <Products />
                
              </Grid>
              <Grid item xs={2} sm={4} md={4} > 
                <Products />
                
              </Grid>
              <Grid item xs={2} sm={4} md={4} > 
                <Products />
                
              </Grid>
              <Grid item xs={2} sm={4} md={4} > 
                <Products />
                
              </Grid>
              <Grid item xs={2} sm={4} md={4} > 
                <Products />
                
              </Grid>
              <Grid item xs={2} sm={4} md={4} > 
                <Products />
                
              </Grid>
          </Grid>

            <Copyright sx={{ pt: 4 }} />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default function Dashboard() {
  return <DashboardContent />;
}
