import React, { useState } from 'react';
import {
    Container,
    Box,
    TextField,
    Button,
    Typography,
    Paper,
} from '@mui/material';

const LoginPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Handle login logic here
        alert(`Email: ${email}\nPassword: ${password}`);
    };

    return (
        <Container maxWidth="sm">
            <Paper elevation={3} sx={{ mt: 8, p: 4 }}>
                <Typography variant="h5" component="h1" gutterBottom>
                    Login
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate>
                   
                    <TextField
                        label="Email"
                        type="email"
                        fullWidth
                        margin="normal"
                        required
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    />
                    <TextField
                        label="Password"
                        type="password"
                        fullWidth
                        margin="normal"
                        required
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    />
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        fullWidth
                        sx={{ mt: 2 }}
                    >
                        Login
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};

export default LoginPage;