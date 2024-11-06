import { useContext } from "react";
import { Grid, Typography, Container } from "@mui/material";
import { MovieCard } from "../MovieCard/MovieCard";
import { AuthContext } from "../../context/AuthContext.jsx";

export const Watchlist = () => {
  const { watchlist } = useContext(AuthContext);
  console.log(watchlist);

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Your Watchlist
      </Typography>
      {watchlist.length > 0 ? (
        <Grid container spacing={4}>
          {watchlist.map((movie) => (
            <Grid item key={movie.movie_id} xs={12} sm={6} md={4} lg={3}>
              <MovieCard
                movie={{
                  id: movie.movie_id,
                  title: movie.omdb_title,
                  rating: movie.omdb_rating,
                  year: movie.omdb_year,
                  description: movie.omdb_plot,
                  poster: movie.omdb_poster,
                }}
              />{" "}
            </Grid>
          ))}
        </Grid>
      ) : (
        <Typography variant="h6" color="textSecondary">
          Your watchlist is empty. Start adding some movies!
        </Typography>
      )}
    </Container>
  );
};
