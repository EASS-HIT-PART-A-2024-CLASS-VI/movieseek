import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../components/MoviePage.css"; // ✅ Corrected path to components directory

const MoviePage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [movie, setMovie] = useState(null);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState("");

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
                credentials: "include",
                headers: { "Content-Type": "application/json" },
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

    if (error) return <p className="error-message">{error}</p>;

    return (
        <div className="movie-page-container">
            {movie ? (
                <>
                    <div className="movie-left">
                        <img src={movie.poster} alt={movie.name} className="movie-poster" />
                        <h1 className="movie-title">{movie.name} ({movie.year})</h1>
                        <p className="movie-genres">🎭 {movie.genres?.join(", ") || "No genres available"}</p>

                        <button onClick={handleSaveMovie} className="save-button">⭐ Save Movie</button>
                        <button onClick={() => navigate(-1)} className="back-button">⬅️ Back to Home</button>

                        {message && <p className="message">{message}</p>}
                    </div>

                    <div className="movie-right">
                        {movie.trailer ? (
                            <iframe
                                className="movie-trailer"
                                src={movie.trailer.replace("watch?v=", "embed/")}
                                title="Movie Trailer"
                                frameBorder="0"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowFullScreen
                            ></iframe>
                        ) : (
                            <p className="no-trailer">🎬 No trailer available</p>
                        )}
                        <p className="movie-description">{movie.description}</p>
                    </div>
                </>
            ) : (
                <p>Loading movie details...</p>
            )}
        </div>
    );
};

export default MoviePage;
