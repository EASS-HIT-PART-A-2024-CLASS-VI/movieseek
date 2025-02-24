import React, { useEffect, useState } from "react";
import MovieCard from "../components/MovieCard"; // ✅ Reusable movie component
import "../components/Home.css"; // ✅ Ensure consistent styles

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
                setSavedMovies(savedMovies.filter((movie) => movie.movie_name !== movieName));
            } else {
                setMessage(`❌ Error removing movie.`);
            }
        } catch (err) {
            setMessage("❌ Failed to remove movie");
        }
    };

    return (
        <div className="container">
            <h2>🎞️ Your Saved Movies</h2>

            {error && <p className="error-message">{error}</p>}
            {message && <p className="message">{message}</p>}

            <div className="trending-movies">
                {savedMovies.length > 0 ? (
                    savedMovies.map((movie) => (
                        <MovieCard 
                            key={movie.movie_name} 
                            movie={movie} 
                            onRemove={handleRemoveMovie} // ✅ Pass remove function
                            showRemoveButton={true} // ✅ Enable remove button
                        />
                    ))
                ) : (
                    <p className="no-movies">No saved movies yet. Start adding some!</p>
                )}
            </div>
        </div>
    );
};

export default SavedMovies;
