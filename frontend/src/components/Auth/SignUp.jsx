import { useContext, useState } from "react";
import {
  Container,
  TextField,
  Button,
  RadioGroup,
  FormControlLabel,
  Radio,
  Checkbox,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormGroup,
  Typography,
  Box,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { genres, occupations } from "../../constants.js";
import { AuthContext } from "../../context/AuthContext.jsx";

export const SignUp = () => {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    age: "",
    gender: "",
    occupation: "",
    preferred_genre: [],
    email: "",
    username: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();
  const { signup } = useContext(AuthContext);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleGenreChange = (e) => {
    const { value, checked } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      preferred_genre: checked
        ? [...prevState.preferred_genre, value]
        : prevState.preferred_genre.filter((genre) => genre !== value),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate the form inputs (you can add more validation as needed)
    if (!formData.gender) {
      setErrors({ gender: "Gender is required." });
      return;
    }

    if (!formData.password || formData.password.length < 8) {
      setErrors({ password: "Password must be at least 8 characters." });
      return;
    }
    const formattedData = {
      ...formData,
      age: formData.age ? parseInt(formData.age) : 0,
      preferred_genre: formData.preferred_genre.join(", "),
    };

    try {
      const response = signup(formattedData);
      console.log("User registered successfully:", response);
      navigate("/signin");
    } catch (error) {
      console.error("Error registering user:", error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" gutterBottom>
        Sign Up
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          label="First Name"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
          margin="normal"
          required
        />
        <TextField
          fullWidth
          label="Last Name"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
          margin="normal"
          required
        />
        <TextField
          fullWidth
          label="Age"
          name="age"
          type="number"
          value={formData.age}
          onChange={handleChange}
          margin="normal"
          inputProps={{ min: 0 }}
        />
        <FormControl component="fieldset" margin="normal">
          <RadioGroup
            row
            aria-label="gender"
            name="gender"
            value={formData.gender}
            onChange={handleChange}
          >
            <FormControlLabel value="male" control={<Radio />} label="Male" />
            <FormControlLabel
              value="female"
              control={<Radio />}
              label="Female"
            />
          </RadioGroup>
          {errors.gender && (
            <Typography color="error">{errors.gender}</Typography>
          )}
        </FormControl>
        <FormControl fullWidth margin="normal">
          <InputLabel>Occupation</InputLabel>
          <Select
            name="occupation"
            value={formData.occupation}
            onChange={handleChange}
          >
            {occupations.map((occupation, index) => (
              <MenuItem key={index} value={occupation.value}>
                {occupation.display}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl component="fieldset" margin="normal">
          <Typography variant="h6">Preferred Genre(s)</Typography>
          <FormGroup row>
            {genres.map((genre) => (
              <FormControlLabel
                key={genre}
                control={
                  <Checkbox
                    value={genre}
                    checked={formData.preferred_genre.includes(genre)}
                    onChange={handleGenreChange}
                  />
                }
                label={genre}
              />
            ))}
          </FormGroup>
        </FormControl>
        <TextField
          fullWidth
          label="Email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          margin="normal"
          required
        />
        <TextField
          fullWidth
          label="Username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          margin="normal"
          required
        />
        <TextField
          fullWidth
          label="Password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          margin="normal"
          required
          error={!!errors.password}
          helperText={errors.password}
        />
        <Box mt={2}>
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Sign Up
          </Button>
        </Box>
      </form>
      <Box mt={2}>
        <Typography>
          Already have an account?{" "}
          <Button onClick={() => navigate("/signin")}>Sign In</Button>
        </Typography>
      </Box>
    </Container>
  );
};
