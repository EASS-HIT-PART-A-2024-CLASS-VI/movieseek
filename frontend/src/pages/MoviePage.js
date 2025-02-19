import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const MoviePage = () => {
    const { id } = useParams(); // ✅ Get the movie ID from the URL
    const navigate = useNavigate();
    const [movie, setMovie] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchMovieDetails = async () => {
            try {
                console.log(`Fetching movie with ID: ${id}`); // ✅ Debugging Step: Check if correct ID is used
                const response = await fetch(`http://localhost:8000/movies/${id}`);
                const data = await response.json();

                if (data.error) {
                    setError("Movie not found");
                } else {
                    setMovie(data);
                }
            } catch (err) {
                setError("Error fetching movie details");
            }
        };

        fetchMovieDetails();
    }, [id]);

    if (error) {
        return <p className="error-message">{error}</p>;
    }

    return (
        <div className="movie-details-container">
            {movie ? (
                <>
                    <h1>{movie.name} ({movie.year})</h1>
                    <img src={movie.poster} alt={movie.name} className="movie-poster" />
                    <p>{movie.description}</p>
                    <button onClick={() => navigate(-1)} className="back-button">⬅️ Back to Home</button>
                </>
            ) : (
                <p>Loading movie details...</p>
            )}
        </div>
    );
};

export default MoviePage;
