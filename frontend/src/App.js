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
  const navigate = useNavigate();
  const hideNav = location.pathname === "/" || location.pathname === "/register";

  const handleLogout = async () => {
    try {
      await fetch("http://localhost:8000/logout", {
        method: "POST",
        credentials: "include",
      });
      navigate("/");
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    !hideNav && (
      <nav className="top-navbar">
        {/* ✅ Entire Logo is Clickable */}
        <Link to="/home" className="logo-container">
          <div className="full-logo-click">
            <img src="/MovieSeekLogo.png" alt="Movie Seek Logo" className="navbar-logo" />
          </div>
        </Link>

        {/* ✅ Navigation Buttons (Centered) */}
        <div className="nav-links">
          <Link to="/home" className="nav-button">🏠 Home</Link>
          <Link to="/saved-movies" className="nav-button">⭐ Saved Movies</Link>
          <button className="nav-button logout-button" onClick={handleLogout}>🚪 Logout</button>
        </div>
      </nav>
    )
  );
}

function App() {
  return (
    <Router>
      <Navigation />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

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
