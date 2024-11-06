import { Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext.jsx";

export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);

  if (!isAuthenticated) {
    // If the user is not authenticated, redirect to the sign-in page
    return <Navigate to="/signin" />;
  }

  // If the user is authenticated, allow access to the protected route
  return children;
};
