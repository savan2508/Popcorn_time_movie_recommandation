import { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import {
  Box,
  Typography,
  Grid,
  Card,
  CardMedia,
  CircularProgress,
} from "@mui/material";
import { MovieCard } from "../components/MovieCard/MovieCard";
import HorizontalScrollList from "../components/HorizontalScrollList/HorizontalScrollList.jsx";
import { AuthContext } from "../context/AuthContext.jsx";

export const MoviePage = () => {
  const { movieId } = useParams();
  const movieIdInt = parseInt(movieId);
  const [movieDetails, setMovieDetails] = useState(null);
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const { isAuthenticated } = useContext(AuthContext);

  useEffect(() => {
    const fetchMovieDetails = async () => {
      setLoading(true);
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/movies_recommendation/recommend_movies",
          {
            movie_input: movieIdInt,
            top_n: 10,
          },
        );
        setMovieDetails(response.data[0].movie);
        setRecommendedMovies(response.data[0].recommended_movies);
        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch movie details:", error);
        setLoading(false);
      }
    };

    fetchMovieDetails();
  }, [movieId]);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="80vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (!movieDetails) {
    return null; // or display some fallback content
  }

  return (
    <>
      {loading ? (
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          minHeight="80vh"
        >
          <CircularProgress /> {/* Loading indicator */}
        </Box>
      ) : (
        <Box p={3}>
          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardMedia
                  sx={{
                    height: 450,
                  }}
                  component="img"
                  image={movieDetails.omdb_poster}
                  alt={movieDetails.omdb_title}
                />
              </Card>
            </Grid>
            <Grid item xs={12} md={8}>
              <Typography variant="h4" gutterBottom>
                {movieDetails.omdb_title}
              </Typography>
              <Typography variant="h6" gutterBottom>
                IMDB Rating: {movieDetails.omdb_imdbRating}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Director: {movieDetails.omdb_director}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Cast: {movieDetails.omdb_actors}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Genres: {movieDetails.genres}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Runtime: {movieDetails.omdb_runtime}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Box Office: {movieDetails.omdb_boxOffice}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Release Date: {movieDetails.omdb_released}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Country: {movieDetails.omdb_country}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Rated: {movieDetails.omdb_rated}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Runtime: {movieDetails.omdb_runtime}
              </Typography>
              <Typography variant="body1" gutterBottom>
                {movieDetails.omdb_plot}
              </Typography>
            </Grid>
          </Grid>

          <HorizontalScrollList
            title={"Recommended Movies"}
            movies={recommendedMovies}
            isAuthenticated={isAuthenticated}
          />
          {/*<Box mt={4}>*/}
          {/*  <Typography variant="h5" gutterBottom>*/}
          {/*    Recommended Movies*/}
          {/*  </Typography>*/}
          {/*  <Box sx={{ display: "flex", overflowX: "auto" }}>*/}
          {/*    {recommendedMovies.map((movie) => (*/}
          {/*      <Box*/}
          {/*        key={movie.movie_id}*/}
          {/*        sx={{ minWidth: 200, marginRight: 2 }}*/}
          {/*      >*/}
          {/*        <MovieCard*/}
          {/*          movie={{*/}
          {/*            id: movie.movie_id,*/}
          {/*            title: movie.omdb_title,*/}
          {/*            year: movie.omdb_year,*/}
          {/*            rating: movie.omdb_imdbRating,*/}
          {/*            description: movie.omdb_plot,*/}
          {/*            poster: movie.omdb_poster,*/}
          {/*          }}*/}
          {/*        />*/}
          {/*      </Box>*/}
          {/*    ))}*/}
          {/*  </Box>*/}
          {/*</Box>*/}
        </Box>
      )}
    </>
  );
};
