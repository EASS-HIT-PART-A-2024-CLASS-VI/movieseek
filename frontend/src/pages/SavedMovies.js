import React, { useEffect, useState } from "react";

const SavedMovies = () => {
    const [savedMovies, setSavedMovies] = useState([]);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState("");

    useEffect(() => {
        const fetchSavedMovies = async () => {
            try {
                const response = await fetch("http://localhost:8000/saved-movies", {
                    method: "GET",
                    credentials: "include", // ✅ Send authentication cookies
                });

                const data = await response.json();
                if (response.ok) {
                    setSavedMovies(data);
                } else {
                    setError("Failed to fetch saved movies");
                }
            } catch (err) {
                setError("Error fetching saved movies");
            }
        };

        fetchSavedMovies();
    }, []);

    const handleRemoveMovie = async (movieName) => {
        try {
            const response = await fetch(`http://localhost:8000/remove-movie/${movieName}`, {
                method: "DELETE",
                credentials: "include",
            });

            if (response.ok) {
                setMessage(`✅ Movie "${movieName}" removed!`);
                setSavedMovies(savedMovies.filter((movie) => movie.movie_name !== movieName));
            } else {
                setMessage(`❌ Error removing movie.`);
            }
        } catch (err) {
            setMessage("❌ Failed to remove movie");
        }
    };

    return (
        <div>
            <h2>🎞️ Saved Movies</h2>

            {error && <p className="error-message">{error}</p>}
            {message && <p className="message">{message}</p>}

            <div className="saved-movies">
                {savedMovies.length > 0 ? (
                    savedMovies.map((movie, index) => (
                        <div key={index} className="movie-card">
                            <img src={movie.movie_poster} alt={movie.movie_name} className="movie-thumbnail" />
                            <h3>{movie.movie_name} ({movie.movie_year})</h3>
                            <p>{movie.movie_description}</p>
                            <button onClick={() => handleRemoveMovie(movie.movie_name)} className="remove-button">
                                ❌ Remove
                            </button>
                        </div>
                    ))
                ) : (
                    <p>No saved movies yet.</p>
                )}
            </div>
        </div>
    );
};

export default SavedMovies;
