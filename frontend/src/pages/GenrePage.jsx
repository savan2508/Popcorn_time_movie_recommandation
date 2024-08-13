import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import MovieGrid from "../components/MovieGrid/MovieGrid.jsx";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { CircularProgress } from "@mui/material";

export const GenrePage = () => {
  const { genre } = useParams();
  const [mostRatedMovies, setMostRatedMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          `http://127.0.0.1:5000/movies_recommendation/${genre}/top_rated`,
        );
        console.log(response);
        setMostRatedMovies(response.data.most_rated_movies);
        setTopRatedMovies(response.data.top_rated_movies);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching genre movies:", error);
        setLoading(false);
      }
    };

    fetchMovies();
  }, []);

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
        <>
          <MovieGrid
            title={`Top Rated ${genre} Movies`}
            movies={topRatedMovies}
          />
          <MovieGrid
            title={`Most Watched ${genre} Movies`}
            movies={mostRatedMovies}
          />
        </>
      )}
    </div>
  );
};
