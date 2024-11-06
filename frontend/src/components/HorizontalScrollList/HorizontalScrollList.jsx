import { Box } from "@mui/material";
import { MovieCard } from "../MovieCard/MovieCard";

const HorizontalScrollList = ({ title, movies, isAuthenticated }) => {
  return (
    <Box sx={{ position: "relative", mt: 4, mb: 4 }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <h2>{title}</h2>
      </Box>
      <Box
        key={title}
        sx={{
          display: "flex",
          overflowX: "auto",
          overflowY: "hidden", // Ensure no vertical scrolling
          scrollBehavior: "smooth",
          whiteSpace: "nowrap",
          "&::-webkit-scrollbar": {
            height: "8px", // Make scrollbar thinner
          },
          "&::-webkit-scrollbar-thumb": {
            backgroundColor: "rgba(0, 0, 0, 0.5)", // Thumb color
            borderRadius: "10px", // Rounded corners
          },
          "&::-webkit-scrollbar-thumb:hover": {
            backgroundColor: "rgba(0, 0, 0, 0.7)", // Darker on hover
          },
          "&::-webkit-scrollbar-track": {
            backgroundColor: "rgba(0, 0, 0, 0.1)", // Track color
          },
          "scrollbar-width": "thin", // Firefox scrollbar size
          "scrollbar-color": "rgba(0, 0, 0, 0.5) rgba(0, 0, 0, 0.1)", // Firefox scrollbar color
        }}
      >
        {movies?.map((movie) => (
          <Box key={movie.movie_id} sx={{ flex: "0 0 auto", marginRight: 2 }}>
            <MovieCard
              provideWidth={200}
              movie={{
                id: movie.movie_id,
                title: movie.omdb_title,
                rating: movie.omdb_imdbRating,
                year: movie.omdb_year,
                description: movie.omdb_plot,
                poster: movie.omdb_poster,
              }}
              isAuthenticated={isAuthenticated}
            />
          </Box>
        ))}
      </Box>
    </Box>
  );
};

export default HorizontalScrollList;
