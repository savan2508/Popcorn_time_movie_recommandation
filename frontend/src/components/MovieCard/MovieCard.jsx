import {
  Card,
  CardActionArea,
  CardMedia,
  CardContent,
  Typography,
  CardActions,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import IconButton from "@mui/material/IconButton";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import InfoIcon from "@mui/icons-material/Info";
import * as PropTypes from "prop-types";
import StarRateIcon from "@mui/icons-material/StarRate";
import { useTheme } from "@mui/material/styles";
import { AuthContext } from "../../context/AuthContext.jsx";
import { useContext, useEffect, useState } from "react";

StarRateIcon.propTypes = { color: PropTypes.string };

export const MovieCard = ({ movie, provideWidth }) => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isDarkMode = theme.palette.mode === "dark";
  const [onWatchlist, setOnWatchlist] = useState(false);
  const { watchlist, addToWatchlist, removeFromWatchlist, isAuthenticated } =
    useContext(AuthContext);

  const handleAddToWatchlist = async () => {
    if (isAuthenticated) {
      await addToWatchlist(movie.id);
      setOnWatchlist(true);
      console.log("Add to Watchlist", movie.title);
    } else {
      navigate("/signin");
    }
  };
  const handleRemoveFromWatchlist = async () => {
    try {
      await removeFromWatchlist(movie.id);
      setOnWatchlist(false);
    } catch (error) {
      console.error("Failed to remove from watchlist:", error);
    }
  };
  useEffect(() => {
    setOnWatchlist(watchlist.some((item) => item.movie_id === movie.id));
  }, [watchlist, movie.id]);

  return (
    <Card
      sx={{
        width: provideWidth ? provideWidth : "auto",
        height: 500,
        m: 1,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        background: isDarkMode
          ? "#424242"
          : "linear-gradient(145deg, #e6e6e6, #ffffff)",
        boxShadow: isDarkMode
          ? "none"
          : "5px 5px 10px #aaaaaa, -5px -5px 10px #ffffff",
        borderRadius: "15px",
        transition: "transform 0.2s",
        "&:hover": {
          transform: "scale(1.05)",
        },
      }}
    >
      <CardActionArea onClick={() => navigate(`/movies/${movie.id}`)}>
        <CardMedia
          component="img"
          height="300" // Fixed height for the image
          image={movie.poster}
          alt={movie.title}
        />
        <CardContent>
          <Typography
            gutterBottom
            variant="h6"
            component="div"
            sx={{ height: 64, overflow: "hidden" }}
          >
            {movie.title}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {movie.year}
          </Typography>
          <Typography
            display="flex"
            alignItems="center"
            variant="body2"
            color="text.secondary"
          >
            <StarRateIcon color="primary" />
            {movie.rating}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions sx={{ display: "flex", justifyContent: "space-between" }}>
        {onWatchlist ? (
          <IconButton
            onClick={handleRemoveFromWatchlist}
            color="primary"
            aria-label="remove from watchlist"
          >
            <RemoveIcon />
          </IconButton>
        ) : (
          <IconButton
            onClick={handleAddToWatchlist}
            color="primary"
            aria-label="add to watchlist"
          >
            <AddIcon />
          </IconButton>
        )}
        <IconButton
          color="primary"
          aria-label="more info"
          onClick={() => navigate(`/movies/${movie.id}`)}
        >
          <InfoIcon />
        </IconButton>
      </CardActions>
    </Card>
  );
};
