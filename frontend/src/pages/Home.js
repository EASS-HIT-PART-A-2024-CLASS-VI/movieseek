import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate for redirection
import "../components/Home.css";
import TrendingMovies from "../components/TrendingMovies";
import MovieSearch from "../components/MovieSearch";

const Home = () => {
    const [movieData, setMovieData] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // Hook for navigation

    // Logout function
    const handleLogout = async () => {
        try {
            await fetch("http://localhost:8000/logout", {
                method: "POST",
                credentials: "include", // Ensure cookies are included for logout
            });

            navigate("/"); // Redirect to login after logout
        } catch (error) {
            console.error("Logout error:", error);
        }
    };

    return (
        <div className="container">
            {/* Logout Button */}
            <div className="logout-container">
                <button onClick={handleLogout} className="logout-button">
                    Logout
                </button>
            </div>

            {/* Movie Search Section */}
            <MovieSearch setMovieData={setMovieData} setError={setError} />

            {error && <p className="error-message">{error}</p>}

            {movieData && (
                <div className="movie-info">
                    <h2>{movieData.name} ({movieData.year})</h2>
                    <img src={movieData.poster} alt={movieData.name} className="movie-poster" />
                    <p>{movieData.description}</p>
                </div>
            )}

            {/* Trending Movies Section */}
            <TrendingMovies />
        </div>
    );
};

export default Home;
