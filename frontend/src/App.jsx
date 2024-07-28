import { useEffect, useState } from "react";
import { Navbar } from "./components/Navbar";
import { Container } from "./components/Container";
import { tempMovieData, tempWatchedData } from "./data/movieData";
import { ListBox, MovieList } from "./components/ListBox";
import { WatchedMovieList, WatchedSummery } from "./components/WatchedBox";
import { Loader } from "./components/Loader.jsx";
import { ErrorMessage } from "./components/ErrorMessage.js";

const omdbAPI = import.meta.env.VITE_OMDB_API;

export default function App() {
  const [movies, setMovies] = useState(tempMovieData);
  const [watched, setWatched] = useState(tempWatchedData);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const searchQuary = "batman";
  useEffect(() => {
    const getMovies = async () => {
      try {
        setIsLoading(true);
        const res = await fetch(
          `https://www.omdbapi.com/?s=${searchQuary}&apikey=${omdbAPI}`,
        );

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();

        if (data.Response === "False") throw new Error("No movies found");
        setMovies(data.Search);
        setIsLoading(false);
      } catch (error) {
        console.error(error.message);
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };
    getMovies();
  }, []);

  return (
    <>
      <Navbar movies={movies} />
      <Container>
        <ListBox>
          {/*{isLoading ? <Loader /> : <MovieList movies={movies} />}*/}
          {isLoading && <Loader />}
          {!isLoading && !error && <MovieList movies={movies} />}
          {error && <ErrorMessage message={error.message} />}
        </ListBox>
        <ListBox>
          <>
            <WatchedSummery watched={watched} />
            <WatchedMovieList watched={watched} />
          </>
        </ListBox>
        {/*<WatchedBox />*/}
      </Container>
    </>
  );
}
