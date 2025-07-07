import React from 'react';
import {
  Container,
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Stack,
  Divider,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const handleSignIn = () => {
    navigate('/login');
  };

  const handleSignUp = () => {
    navigate('/signup');
  };

  return (
    <Container>
      <Box
        sx={{
          minHeight: '80vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          py: 4,
        }}
      >
        <Card
          sx={{
            width: '100%',
            maxWidth: 400,
            boxShadow: 3,
            borderRadius: 2,
          }}
        >
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ textAlign: 'center', mb: 3 }}>
              <Typography
                variant="h4"
                component="h1"
                gutterBottom
                sx={{ fontWeight: 'bold', color: 'primary.main' }}
              >
                Welcome to AIoT Tank
              </Typography>
              <Typography
                variant="body1"
                color="text.secondary"
                sx={{ mb: 3 }}
              >
                Control and monitor your smart tank system
              </Typography>
            </Box>

            <Box sx={{ textAlign: 'center', mb: 3 }}>
              <Typography
                variant="h6"
                component="h2"
                gutterBottom
                sx={{ fontWeight: 'medium' }}
              >
                Do you have an account?
              </Typography>
            </Box>

            <Stack spacing={2}>
              <Button
                variant="contained"
                size="large"
                onClick={handleSignIn}
                sx={{
                  py: 1.5,
                  fontSize: '1.1rem',
                  fontWeight: 'medium',
                }}
              >
                Yes, Sign In
              </Button>

              <Divider sx={{ my: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  or
                </Typography>
              </Divider>

              <Button
                variant="outlined"
                size="large"
                onClick={handleSignUp}
                sx={{
                  py: 1.5,
                  fontSize: '1.1rem',
                  fontWeight: 'medium',
                }}
              >
                No, Create Account
              </Button>
            </Stack>

            <Box sx={{ textAlign: 'center', mt: 3 }}>
              <Typography variant="caption" color="text.secondary">
                Join us to start monitoring your tank system
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default HomePage;
