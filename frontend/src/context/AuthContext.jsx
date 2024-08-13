import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

// Create the context
export const AuthContext = createContext();

// Create a provider component
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    // Initialize authentication state from localStorage
    return JSON.parse(localStorage.getItem("isAuthenticated")) || false;
  });
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (isAuthenticated) {
      // Check auth status if authenticated state is true
      const checkAuthStatus = async () => {
        try {
          const response = await axios.post(
            "/auth/refresh_token",
            {},
            { withCredentials: true },
          );
          if (response.data.isAuthenticated) {
            setUser(response.data.user);
          } else {
            setIsAuthenticated(false);
            setUser(null);
          }
        } catch (error) {
          console.error("Failed to refresh token:", error);
          setIsAuthenticated(false);
          setUser(null);
        }
      };

      checkAuthStatus();
    }
  }, [isAuthenticated]);

  const signup = async (signupData) => {
    try {
      const response = await axios.post("/auth/signup", signupData);
      return response.data; // Handle signup response as needed
    } catch (error) {
      console.error("Signup failed:", error);
      throw error;
    }
  };

  const login = async (credentials) => {
    try {
      const response = await axios.post("/auth/signin", credentials, {
        withCredentials: true,
      });
      if (response.data.isAuthenticated) {
        setUser(response.data.user);
        setIsAuthenticated(true);
        localStorage.setItem("isAuthenticated", JSON.stringify(true)); // Store auth status in localStorage
      }
    } catch (error) {
      console.error("Login failed:", error);
      setIsAuthenticated(false);
      localStorage.setItem("isAuthenticated", JSON.stringify(false));
      throw error;
    }
  };

  const logout = async () => {
    try {
      await axios.post("/auth/sign_out", {}, { withCredentials: true });
      setUser(null);
      setIsAuthenticated(false);
      localStorage.setItem("isAuthenticated", JSON.stringify(false)); // Remove auth status from localStorage
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, user, signup, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};
