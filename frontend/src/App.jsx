import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { getTheme } from "./theme";
import { Home } from "./pages/Home";
import { SignIn } from "./components/Auth/SignIn";
import { SignUp } from "./components/Auth/SignUp";
import { Watchlist } from "./components/Watchlist/Watchlist";
import { Recommendations } from "./components/Recommendations/Recommendations";
import { Navbar } from "./components/Navbar/Navbar.jsx";
import {
  ColorModeContext,
  ColorModeProvider,
} from "./context/ColorModeContext.jsx";
import { useContext } from "react";
import { GenrePage } from "./pages/GenrePage.jsx";
import { AuthProvider } from "./context/AuthContext.jsx";
import { MoviePage } from "./pages/MoviePage.jsx";
import { ProtectedRoute } from "./components/ProtecteRoute/ProtectedRoute.jsx";
import Account from "./pages/Account.jsx";

const App = () => {
  return (
    <ColorModeProvider>
      <AppContent />
    </ColorModeProvider>
  );
};

const AppContent = () => {
  const { mode } = useContext(ColorModeContext);
  const theme = getTheme(mode);
  return (
    <ThemeProvider theme={theme}>
      <AuthProvider>
        <CssBaseline />
        <Router>
          <Navbar />
          <Routes>
            <Route index element={<Home />} />
            <Route path="/genre/:genre" element={<GenrePage />} />
            <Route path="/movies/:movieId" element={<MoviePage />} />
            <Route path="/signin" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
            {/*<Route path="/watchlist" element={<Watchlist />} />*/}
            {/*<Route path="/recommendations" element={<Recommendations />} />*/}
            <Route
              path="/account"
              element={
                <ProtectedRoute>
                  <Account />
                </ProtectedRoute>
              }
            />
            {/*<Route*/}
            {/*  path="/recommendations"*/}
            {/*  element={*/}
            {/*    <ProtectedRoute>*/}
            {/*      <Recommendations />*/}
            {/*    </ProtectedRoute>*/}
            {/*  }*/}
            {/*/>*/}
            <Route
              path="/watchlist"
              element={
                <ProtectedRoute>
                  <Watchlist />
                </ProtectedRoute>
              }
            />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
