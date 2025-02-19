import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import MoviePage from "./pages/MoviePage"; 
import ProtectedRoute from "./components/ProtectedRoute"; 

function App() {
  return (
    <Router>
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
        /> {/* ✅ Protects movie page */}
      </Routes>
    </Router>
  );
}

export default App;
