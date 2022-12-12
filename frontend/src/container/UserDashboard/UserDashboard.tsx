import * as React from 'react';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import MuiDrawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import Avatar from '@mui/material/Avatar';
import Orders from './Orders';
import PersonalInfo from './PersonalInfo';
// import ProfilePic from './ProfilePic';
import Button from '@mui/material/Button';
import TopBar from './TopBar';
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
            <Grid container spacing={3}>
              {/* Profile picture */}
              <Grid item xs={4} md={4} lg={3}>
                  <Avatar
                    alt="prfile picture"
                    src="http://gavel.mrt.ac.lk/wp-content/uploads/2022/02/WhatsApp-Image-2022-02-06-at-8.17.07-PM-150x150.jpeg"
                  sx={{
                    height: 230,
                    width: 180,
                    margin: 'auto',
                    boxShadow: 20,
                  }}
                  />
                {/* <ProfilePic /> */}
              </Grid>
              {/* Personal info */}
              <Grid item xs={8} md={8} lg={9}>
                  <PersonalInfo />
              </Grid>
              {/* Recent Orders */}
              <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                  <Orders />
                </Paper>
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
