import React, { useEffect, useState } from "react";
import MovieCard from "../components/MovieCard"; // ✅ Reusable MovieCard component
import "../components/Home.css"; // ✅ Consistent styling
import "../components/TextStyles.css"; // ✅ Import the text styling component

const SavedMovies = () => {
    const [savedMovies, setSavedMovies] = useState([]);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState("");

    useEffect(() => {
        const fetchSavedMovies = async () => {
            try {
                const response = await fetch("http://localhost:8000/saved-movies", { 
                    method: "GET",
                    credentials: "include",
                });                

                if (!response.ok) {
                    throw new Error("Failed to fetch saved movies");
                }

                const data = await response.json();
                console.log("Fetched Saved Movies:", data); // ✅ Debugging log
                setSavedMovies(data);
            } catch (err) {
                console.error("Error fetching saved movies:", err);
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
                setMessage(`✅ Removed "${movieName}" successfully!`);
            } else {
                setMessage("❌ Error removing movie.");
            }
        } catch (err) {
            console.error("Remove movie error:", err);
            setMessage("❌ Failed to remove movie.");
        }
    };

    return (
        <div className="container">
            {/* ✅ Centered & Styled Heading */}
            <h2 className="text-stroke text-bold text-large saved-movies-title">
                🎞️ Your Saved Movies
            </h2>

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
