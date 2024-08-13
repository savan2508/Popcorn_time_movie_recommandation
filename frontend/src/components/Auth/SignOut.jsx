import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { AppBar, Box, Button, Toolbar, Typography } from "@mui/material";

export const Navbar = () => {
  const { isAuthenticated, logout } = useContext(AuthContext);

  const handleLogout = async () => {
    try {
      await logout();
      // Redirect or update state as needed after logout
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          My Application
        </Typography>
        {isAuthenticated ? (
          <Button color="inherit" onClick={handleLogout}>
            Sign Out
          </Button>
        ) : (
          <Button color="inherit" href="/signin">
            Sign In
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
};
