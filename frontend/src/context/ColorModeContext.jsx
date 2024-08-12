import { createContext, useState } from "react";
import { useMediaQuery } from "@mui/material";

export const ColorModeContext = createContext();

export const ColorModeProvider = ({ children }) => {
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
  console.log("prefersDarkMode", prefersDarkMode);
  const [mode, setMode] = useState("dark");
  const ToggleColorMode = () => {
    setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
  };
  return (
    <ColorModeContext.Provider
      value={{
        mode: mode,
        ToggleColorMode,
      }}
    >
      {children}
    </ColorModeContext.Provider>
  );
};
