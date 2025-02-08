import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/protected", {
      method: "GET",
      credentials: "include", // Include cookies for authentication check
    })
      .then((response) => {
        if (response.ok) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      })
      .catch(() => setIsAuthenticated(false));
  }, []);

  if (isAuthenticated === null) return <p>Loading...</p>; // Prevents flickering

  return isAuthenticated ? children : <Navigate to="/" />;
};

export default ProtectedRoute;
