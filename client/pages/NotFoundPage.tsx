import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const NotFound: React.FC = () => {
    const navigate = useNavigate();

    return (
        <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            minHeight="100vh"
            bgcolor="background.default"
        >
            <Typography variant="h2" color="primary" gutterBottom>
                404
            </Typography>
            <Typography variant="h5" gutterBottom>
                Page Not Found
            </Typography>
            <Typography variant="body1" color="textSecondary" mb={3}>
                The page you are looking for does not exist.
            </Typography>
            <Button variant="contained" color="primary" onClick={() => navigate('/')}>
                Go Home
            </Button>
        </Box>
    );
};

export default NotFound;