import React from "react";
import { BrowserRouter as Router, Route, Routes, Link, useLocation, useNavigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import MoviePage from "./pages/MoviePage"; 
import SavedMovies from "./pages/SavedMovies"; 
import ProtectedRoute from "./components/ProtectedRoute"; 
import "./App.css"; 

function Navigation() {
  const location = useLocation();
  const navigate = useNavigate(); // ✅ Moved useNavigate inside Navigation component
  const hideNav = location.pathname === "/" || location.pathname === "/register";

  const handleLogout = async () => {
    try {
      await fetch("http://localhost:8000/logout", {
        method: "POST",
        credentials: "include",
      });
      navigate("/"); // ✅ Redirects to login after logout
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    !hideNav && (
      <nav className="top-navbar">
        <Link to="/home" className="nav-button">🏠 Home</Link>
        <Link to="/saved-movies" className="nav-button">⭐ Saved Movies</Link>
        <button className="nav-button logout-button" onClick={handleLogout}>🚪 Logout</button>
      </nav>
    )
  );
}

function App() {
  return (
    <Router>
      <Navigation /> {/* ✅ Moved inside Router to fix useNavigate issue */}
      <Routes>
        {/* ✅ Public Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* ✅ Protected Routes */}
        <Route 
          path="/home"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/movie/:id"
          element={
            <ProtectedRoute>
              <MoviePage />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/saved-movies"
          element={
            <ProtectedRoute>
              <SavedMovies />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
