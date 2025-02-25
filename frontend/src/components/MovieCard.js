import React from "react";
import "../components/Home.css"; // ✅ Import CSS for styling

const MovieCard = ({ movie, onRemove, showRemoveButton }) => {
    return (
        <div className="movie-card">
            <img src={movie.movie_poster} alt={movie.movie_name} className="movie-thumbnail" />
            <div className="movie-details">
                <h3>{movie.movie_name} ({movie.movie_year})</h3>
                <p>{movie.movie_description}</p>

                {/* ✅ Styled Remove Button */}
                {showRemoveButton && (
                    <button onClick={() => onRemove(movie.movie_name)} className="remove-button">
                        Remove
                    </button>
                )}
            </div>
        </div>
    );
};

export default MovieCard;
