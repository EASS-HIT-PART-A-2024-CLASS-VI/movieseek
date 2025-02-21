import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const MoviePage = () => {
    const { id } = useParams(); // Get the movie ID from the URL
    const navigate = useNavigate();
    const [movie, setMovie] = useState(null);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState(""); // ✅ State for success/error messages

    useEffect(() => {
        const fetchMovieDetails = async () => {
            try {
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

    const handleSaveMovie = async () => {
        if (!movie) return;

        try {
            const response = await fetch("http://localhost:8000/save-movie", {
                method: "POST",
                credentials: "include", // ✅ Send cookies (authentication)
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    movie_name: movie.name,
                    movie_year: movie.year,
                    movie_description: movie.description,
                    movie_poster: movie.poster,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                setMessage("✅ Movie saved successfully!");
            } else {
                setMessage(`❌ Error: ${data.detail}`);
            }
        } catch (err) {
            setMessage("❌ Failed to save movie");
        }
    };

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

                    {/* ✅ Save Movie Button */}
                    <button onClick={handleSaveMovie} className="save-button">
                        ⭐ Save Movie
                    </button>

                    {/* ✅ Display Success/Error Message */}
                    {message && <p className="message">{message}</p>}

                    <button onClick={() => navigate(-1)} className="back-button">
                        ⬅️ Back to Home
                    </button>
                </>
            ) : (
                <p>Loading movie details...</p>
            )}
        </div>
    );
};

export default MoviePage;
