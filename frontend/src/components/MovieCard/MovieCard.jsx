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
import InfoIcon from "@mui/icons-material/Info";
import * as PropTypes from "prop-types";
import StarRateIcon from "@mui/icons-material/StarRate";

StarRateIcon.propTypes = { color: PropTypes.string };

export const MovieCard = ({ movie, isAuthenticated }) => {
  const navigate = useNavigate();

  const handleAddToWatchlist = () => {
    if (isAuthenticated) {
      // TODO: add the watchlist functionality
      console.log("Add to Watchlist", title);
    } else {
      navigate("/signin");
    }
  };

  return (
    <Card
      sx={{
        // width: 60,
        height: 500,
        m: 1,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
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
        <IconButton
          onClick={handleAddToWatchlist}
          color="primary"
          aria-label="add to watchlist"
        >
          <AddIcon />
        </IconButton>
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
