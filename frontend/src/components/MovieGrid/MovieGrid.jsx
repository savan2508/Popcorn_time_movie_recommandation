import { Grid, Typography, Box } from "@mui/material";
import { MovieCard } from "../MovieCard/MovieCard.jsx";

const MovieGrid = ({ title, movies, isAuthenticated }) => {
  return (
    <Box sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        {title}
      </Typography>
      <Grid container spacing={0.25}>
        {movies.map((movie) => (
          <Grid item key={movie.movie_id} xs={12} sm={6} md={4} lg={2.4}>
            <MovieCard
              movie={{
                id: movie.movie_id,
                title: movie.omdb_title,
                rating: movie.omdb_rating,
                year: movie.omdb_year,
                description: movie.omdb_plot,
                poster: movie.omdb_poster,
              }}
              isAuthenticated={isAuthenticated}
            />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default MovieGrid;
