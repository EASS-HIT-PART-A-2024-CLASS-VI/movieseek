import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch("http://localhost:8000/protected", {
          method: "GET",
          credentials: "include", // ✅ Ensures cookies are sent for session auth
        });

        setIsAuthenticated(response.ok); // ✅ If response.ok is true, user is authenticated
      } catch (error) {
        console.error("Authentication check failed:", error);
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  if (isAuthenticated === null) {
    return <p style={{ textAlign: "center", fontSize: "18px" }}>🔄 Checking authentication...</p>; // ✅ Improved loading UI
  }

  return isAuthenticated ? children : <Navigate to="/" replace />; // ✅ Prevents unnecessary history stacking
};

export default ProtectedRoute;
