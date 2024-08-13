import IconButton from "@mui/material/IconButton";
import Box from "@mui/material/Box";
import { useTheme } from "@mui/material/styles";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { ColorModeContext } from "../../context/ColorModeContext.jsx";
import { useContext } from "react";

export const ColorModeButton = () => {
  const theme = useTheme();
  const { mode, ToggleColorMode } = useContext(ColorModeContext);
  return (
    <IconButton sx={{ ml: 1 }} onClick={ToggleColorMode} color="inherit">
      {theme.palette.mode === "dark" ? (
        <Brightness7Icon />
      ) : (
        <Brightness4Icon />
      )}
    </IconButton>
  );
};
