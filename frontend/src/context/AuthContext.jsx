import { createContext, useState, useEffect } from "react";
import axios from "axios";
import { BASE_URL } from "../constants.js";

// Create the context
export const AuthContext = createContext();

// Create a provider component
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    // Initialize authentication state from localStorage
    return JSON.parse(localStorage.getItem("isAuthenticated")) || false;
  });
  const [user, setUser] = useState(null);
  const [userInfo, setUserInfo] = useState(null);
  const [watchlist, setWatchlist] = useState([]);

  useEffect(() => {
    const fetchWatchlist = async () => {
      try {
        const accessToken = localStorage.getItem("access_token");
        if (accessToken) {
          const response = await axios.get(
            `${BASE_URL}/user_actions/watchlist`,
            {
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            },
          );
          setWatchlist(response.data);
        }
      } catch (error) {
        console.error("Failed to fetch watchlist:", error);
      }
    };

    if (isAuthenticated) {
      fetchWatchlist();
    }
  }, [isAuthenticated]);

  const addToWatchlist = async (movieId) => {
    try {
      const response = await axios.post(
        `${BASE_URL}/user_actions/watchlist`,
        { movie_id: parseInt(movieId, 10) },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );
      setWatchlist([...watchlist, response.data]);
      console.log("Movie added to watchlist:", response.data);
    } catch (error) {
      console.error("Error adding movie to watchlist:", error);
      throw error;
    }
  };

  const removeFromWatchlist = async (movieId) => {
    try {
      await axios.delete(
        `${BASE_URL}/user_actions/watchlist/${parseInt(movieId, 10)}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );
      setWatchlist(watchlist.filter((movie) => movie.movie_id !== movieId));
      console.log("Movie removed from watchlist");
    } catch (error) {
      console.error("Error removing movie from watchlist:", error);
      throw error;
    }
  };

  useEffect(() => {
    fetchUserInfo();
  }, [isAuthenticated]);

  const signup = async (signupData) => {
    console.log("signupData", signupData);
    try {
      const response = await axios.post(BASE_URL + "/auth/signup", signupData, {
        withCredentials: true,
      });
      console.log("User registered successfully:", response);
      return response.data; // Handle signup response as needed
    } catch (error) {
      console.error("Signup failed:", error);
      throw error;
    }
  };

  const fetchUserInfo = async () => {
    try {
      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        return;
      }
      const response = await axios.get(BASE_URL + "/user/info", {
        headers: {
          Authorization: `Bearer ${accessToken}`, // Include the token in the request header
        },
      });
      setUserInfo(response.data);
    } catch (error) {
      console.error("Failed to fetch user info:", error);
    }
  };

  const login = async (credentials) => {
    try {
      const response = await axios.post(
        BASE_URL + "/auth/signin",
        credentials,
        {
          withCredentials: true,
        },
      );
      console.log("response", response);
      if (
        response.data.message === "Login successful" &&
        response.status === 200
      ) {
        setUser(response.data.user);
        setIsAuthenticated(true);
        localStorage.setItem("isAuthenticated", JSON.stringify(true)); // Store auth status in localStorage
        localStorage.setItem("access_token", response.data.access_token); // Store access token in localStorage
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
      await axios.post(
        BASE_URL + "/auth/sign_out",
        {},
        { withCredentials: true },
      );
      setUser(null);
      setIsAuthenticated(false);
      localStorage.setItem("isAuthenticated", JSON.stringify(false)); // Remove auth status from localStorage
      localStorage.removeItem("access_token"); // Remove access token from localStorage
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        signup,
        login,
        logout,
        userInfo,
        watchlist,
        addToWatchlist,
        removeFromWatchlist,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
