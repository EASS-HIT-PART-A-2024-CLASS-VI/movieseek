import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ Import useNavigate

const TrendingMovies = () => {
    const [trendingMovies, setTrendingMovies] = useState([]);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // ✅ Hook for navigation

    useEffect(() => {
        const fetchTrendingMovies = async () => {
            try {
                const response = await fetch("http://localhost:8000/trending-movies");
                const data = await response.json();

                if (data.detail) {
                    setError("Error fetching trending movies");
                } else {
                    setTrendingMovies(data);
                }
            } catch (err) {
                setError("Error fetching trending movies");
            }
        };

        fetchTrendingMovies();
    }, []);

    // ✅ Function to handle clicking on a movie
    const handleMovieClick = (movieName) => {
        navigate(`/movie/${movieName}`); // ✅ Redirect to movie page
    };

    return (
        <div>
            <h2>🔥 Trending Movies</h2>
            {error && <p className="error-message">{error}</p>}
            <div className="trending-movies">
                {trendingMovies.map((movie, index) => (
                    <div 
                        key={index} 
                        className="movie-card"
                        onClick={() => handleMovieClick(movie.name)} // ✅ Click event
                        style={{ cursor: "pointer" }} // ✅ Indicate clickable element
                    >
                        <img src={movie.poster} alt={movie.name} className="movie-thumbnail" />
                        <h3>{movie.name}</h3>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TrendingMovies;
