import { useState, useEffect, useContext } from "react";
import { Container } from "@mui/material";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";
import MovieGrid from "../components/MovieGrid/MovieGrid.jsx"; // Assume you have an AuthContext

export const Home = () => {
  const { isAuthenticated } = useContext(AuthContext);
  const [mostRatedMovies, setMostRatedMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/movies_recommendation/popular",
        );
        setMostRatedMovies(response.data.most_rated_movies);
        setTopRatedMovies(response.data.top_rated_movies);
      } catch (error) {
        console.error("Failed to fetch movies", error);
      }
    };

    fetchMovies();
  }, []);

  return (
    <div>
      <Container>
        <MovieGrid
          title="Most Rated Movies"
          movies={mostRatedMovies}
          isAuthenticated={isAuthenticated}
        />
        <MovieGrid
          title="Top Rated Movies"
          movies={topRatedMovies}
          isAuthenticated={isAuthenticated}
        />
      </Container>
    </div>
  );
};
