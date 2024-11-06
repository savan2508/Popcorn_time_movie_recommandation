import { useContext, useEffect, useState } from "react";
import { Container, Typography, CircularProgress } from "@mui/material";
import axios from "axios";
import { AuthContext } from "../../context/AuthContext";
import HorizontalScrollList from "../HorizontalScrollList/HorizontalScrollList.jsx";
import { BASE_URL } from "../../constants.js";
import Box from "@mui/material/Box";

export const Recommendations = () => {
  const { userInfo, watchlist, isAuthenticated } = useContext(AuthContext);
  const preferredGenres = userInfo.preferred_genre.split(", ");
  const recommendedGenres = userInfo.recommended_genre.split(", ");
  const randomWatchlistMovies = getRandomMovies(watchlist, 10);

  console.log(preferredGenreMovies);
  console.log(recommendedGenreMovies);
  console.log(watchlistRecommendations);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      if (userInfo) {
        setLoading(true);

        await Promise.all(fetchPromises);

        setLoading(false);
      }
    };

    fetchData();
  }, [userInfo, watchlist]);

  const fetchGenreRecommendations = async (genres, type) => {
    try {
      const genreRecs = await Promise.all(
        genres.map(async (genre) => {
          const response = await axios.get(
            `${BASE_URL}/movies_recommendation/${genre}/top_rated`,
          );
          return { genre, movies: response.data };
        }),
      );
      if (type === "preferred") {
        setPreferredGenreMovies(genreRecs);
      } else if (type === "recommended") {
        setRecommendedGenreMovies(genreRecs);
      }
    } catch (error) {
      console.error("Error fetching genre recommendations:", error);
    }
  };

  const fetchWatchlistRecommendations = async (movies) => {
    try {
      const movieTitles = movies.map((movie) => movie.movie_name);
      const response = await axios.post(
        `${BASE_URL}/movies_recommendation/recommend_movies`,
        {
          movie_input: movieTitles,
          top_n: 10,
        },
      );
      setWatchlistRecommendations(response.data);
    } catch (error) {
      console.error("Error fetching watchlist recommendations:", error);
    }
  };

  const getRandomMovies = (movies, n) => {
    const shuffled = [...movies].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, n);
  };

  return (
    <div>
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
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Recommendations for You
          </Typography>

          {preferredGenreMovies.map((genreRec) => (
            <HorizontalScrollList
              key={genreRec.genre}
              title={`Since you prefer ${genreRec.genre}`}
              movies={genreRec.movies}
              isAuthenticated={isAuthenticated}
            />
          ))}

          {recommendedGenreMovies.map((genreRec) => (
            <HorizontalScrollList
              key={genreRec.genre}
              title={`Based on user group recommendations: ${genreRec.genre}`}
              movies={genreRec.movies}
              isAuthenticated={isAuthenticated}
            />
          ))}

          {watchlistRecommendations.length > 0 && (
            <HorizontalScrollList
              title="Since you watched these movies"
              movies={watchlistRecommendations}
              isAuthenticated={isAuthenticated}
            />
          )}
        </Container>
      )}
    </div>
  );
};
