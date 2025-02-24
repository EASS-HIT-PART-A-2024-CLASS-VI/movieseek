import React from "react";
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import MoviePage from "./pages/MoviePage"; 
import SavedMovies from "./pages/SavedMovies"; 
import ProtectedRoute from "./components/ProtectedRoute"; 
import "./App.css"; // ✅ Ensure this line is at the top of App.js

function Navigation() {
  const location = useLocation();
  const hideNav = location.pathname === "/" || location.pathname === "/register"; // ✅ Hide nav on Login/Register

  return (
    !hideNav && ( // ✅ Show navbar only if NOT on login/register
      <nav>
        <Link to="/home">🏠 Home</Link>
        <Link to="/saved-movies">⭐ Saved Movies</Link>
      </nav>
    )
  );
}

function App() {
  return (
    <Router>
      <Navigation /> {/* ✅ Show/hide navigation dynamically */}
      <Routes>
        {/* ✅ Public Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* ✅ Protected Routes (Only for Authenticated Users) */}
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
