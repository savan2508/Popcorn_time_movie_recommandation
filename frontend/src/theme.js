import { createTheme } from "@mui/material/styles";

export const getTheme = (mode) =>
  createTheme({
    palette: {
      mode: mode,
    },
    typography: {
      fontFamily: "Roboto, Arial, sans-serif", // Common fonts used by IMDb
      h6: {
        fontWeight: 700,
      },
      body1: {
        fontSize: "1rem",
        lineHeight: 1.5,
      },
    },
  });
