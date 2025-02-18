import React, { useState } from "react";
import "../components/Home.css";
import TrendingMovies from "../components/TrendingMovies";
import MovieSearch from "../components/MovieSearch";

const Home = () => {
    const [movieData, setMovieData] = useState(null);
    const [error, setError] = useState(null);

    return (
        <div className="container">
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
