import React, { useEffect, useState } from "react";

const TrendingMovies = () => {
    const [trendingMovies, setTrendingMovies] = useState([]);
    const [error, setError] = useState(null);

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

    return (
        <div>
            <h2>🔥 Trending Movies</h2>
            {error && <p className="error-message">{error}</p>}
            <div className="trending-movies">
                {trendingMovies.map((movie, index) => (
                    <div key={index} className="movie-card">
                        <img src={movie.poster} alt={movie.name} className="movie-thumbnail" />
                        <h3>{movie.name}</h3>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TrendingMovies;
