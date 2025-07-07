import React, { useState } from 'react';
import {

Container,
Box,
TextField,
Button,
Typography,
Paper,
} from '@mui/material';

const SignupPage: React.FC = () => {
const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
});

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
};

const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle signup logic here
    alert('Signup submitted!');
};

return (
    <Container maxWidth="sm">
        <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
            <Typography variant="h5" component="h1" gutterBottom>
                Sign Up
            </Typography>
            <Box component="form" onSubmit={handleSubmit} noValidate>
                <TextField
                    margin="normal"
                    fullWidth
                    label="Name"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    required
                />
                <TextField
                    margin="normal"
                    fullWidth
                    label="Email"
                    name="email"
                    type="email"
                    value={form.email}
                    onChange={handleChange}
                    required
                />
                <TextField
                    margin="normal"
                    fullWidth
                    label="Password"
                    name="password"
                    type="password"
                    value={form.password}
                    onChange={handleChange}
                    required
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3 }}
                >
                    Sign Up
                </Button>
            </Box>
        </Paper>
    </Container>
);
};

export default SignupPage;