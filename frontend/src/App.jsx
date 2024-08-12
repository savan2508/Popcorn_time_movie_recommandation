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

const App = () => {
  return (
    <ColorModeProvider>
      <AppContent />
    </ColorModeProvider>
  );
};

const AppContent = () => {
  const { mode } = useContext(ColorModeContext);
  console.log("mode", mode);
  const theme = getTheme(mode);
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <Router>
        <Routes>
          <Route path="/" element={<Navbar />} />
          <Route index={true} element={<Home />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/watchlist" element={<Watchlist />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;
