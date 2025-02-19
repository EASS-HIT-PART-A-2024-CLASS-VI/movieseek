import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../components/Home.css";
import TrendingMovies from "../components/TrendingMovies";
import MovieSearch from "../components/MovieSearch";

const Home = () => {
    const [movieData, setMovieData] = useState(null);
    const [error, setError] = useState(null);
    const [username, setUsername] = useState(""); // Store logged-in user
    const navigate = useNavigate();

    // Fetch authenticated user data
    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch("http://localhost:8000/protected", {
                    method: "GET",
                    credentials: "include", // Include cookies
                });

                if (response.ok) {
                    const data = await response.json();
                    setUsername(data.username); // Extract username from response
                } else {
                    throw new Error("Not authenticated");
                }
            } catch (error) {
                console.error("Authentication error:", error);
                navigate("/"); // Redirect to login if not authenticated
            }
        };

        fetchUser();
    }, [navigate]);

    // Logout function
    const handleLogout = async () => {
        try {
            await fetch("http://localhost:8000/logout", {
                method: "POST",
                credentials: "include",
            });

            navigate("/"); // Redirect to login after logout
        } catch (error) {
            console.error("Logout error:", error);
        }
    };

    return (
        <div className="container">
            <div className="header">
                <h2>Welcome, {username || "User"}!</h2>
                <button onClick={handleLogout} className="logout-button">
                    Logout
                </button>
            </div>

            <MovieSearch setMovieData={setMovieData} setError={setError} />

            {error && <p className="error-message">{error}</p>}

            {movieData && (
                <div className="movie-info">
                    <h2>{movieData.name} ({movieData.year})</h2>
                    <img src={movieData.poster} alt={movieData.name} className="movie-poster" />
                    <p>{movieData.description}</p>
                </div>
            )}

            <TrendingMovies />
        </div>
    );
};

export default Home;
