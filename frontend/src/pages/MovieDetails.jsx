import { useParams } from "react-router-dom";
import { Navbar } from "../components/Navbar/Navbar";
import { Container, Typography, Grid } from "@mui/material";
import MovieCard from "../components/MovieCard/MovieCard.jsx";
import { mockMovies } from "../data.js";

const MovieDetails = () => {
  const { movieId } = useParams();
  const movie = mockMovies.find((m) => m.id === parseInt(movieId));

  // Mock recommendations: exclude the current movie from the recommendations
  const recommendations = mockMovies.filter((m) => m.id !== movie.id);

  return (
    <div>
      <Navbar />
      <Container sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          {movie.title}
        </Typography>
        <Typography variant="body1" gutterBottom>
          {movie.description}
        </Typography>
        <Typography variant="h6" sx={{ mt: 4 }}>
          Recommended Movies
        </Typography>
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {recommendations.map((recMovie) => (
            <Grid item key={recMovie.id} xs={12} sm={6} md={4} lg={3}>
              <MovieCard movie={recMovie} />
            </Grid>
          ))}
        </Grid>
      </Container>
    </div>
  );
};

export default MovieDetails;
