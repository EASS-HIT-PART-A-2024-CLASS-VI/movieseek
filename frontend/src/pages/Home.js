import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../components/Home.css";
import TrendingMovies from "../components/TrendingMovies";
import TopRatedMovies from "../components/TopRatedMovies";
import MovieSearch from "../components/MovieSearch";

const Home = () => {
    const [movieData, setMovieData] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch("http://localhost:8000/protected", {
                    method: "GET",
                    credentials: "include",
                });

                if (!response.ok) {
                    throw new Error("Not authenticated");
                }
            } catch (error) {
                console.error("Authentication error:", error);
                navigate("/");
            }
        };

        fetchUser();
    }, [navigate]);

    return (
        <div className="container">
            {/* ✅ Removed extra logout button */}
            
            {/* Centered Movie Search Bar */}
            <div className="search-container">
                <MovieSearch setMovieData={setMovieData} setError={setError} />
            </div>

            {error && <p className="error-message">{error}</p>}

            {/* Display the searched movie */}
            {movieData && (
                <div className="movie-info">
                    <h2>{movieData.name} ({movieData.year})</h2>
                    <img src={movieData.poster} alt={movieData.name} className="movie-thumbnail" />
                    <p>{movieData.description}</p>
                </div>
            )}

            {/* Trending Movies Section */}
            <div className="section-box">
                <TrendingMovies />
            </div>

            {/* Top Rated Movies Section */}
            <div className="section-box">
                <TopRatedMovies />
            </div>
        </div>
    );
};

export default Home;
