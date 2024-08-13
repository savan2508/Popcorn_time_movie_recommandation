import { useState, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { Box, Button, TextField, Typography } from "@mui/material";

export const SignIn = () => {
  const { login } = useContext(AuthContext);
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await login(credentials);
      // Redirect or update state as needed after successful login
    } catch (error) {
      setError("Invalid username or password");
      console.error("Error signing in:", error);
    }
  };

  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 8, px: 2 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Sign In
      </Typography>
      {error && (
        <Typography color="error" variant="body2" gutterBottom>
          {error}
        </Typography>
      )}
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          label="Username"
          name="username"
          value={credentials.username}
          onChange={handleChange}
          margin="normal"
          required
        />
        <TextField
          fullWidth
          label="Password"
          type="password"
          name="password"
          value={credentials.password}
          onChange={handleChange}
          margin="normal"
          required
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          sx={{ mt: 2 }}
        >
          Sign In
        </Button>
      </form>
    </Box>
  );
};
