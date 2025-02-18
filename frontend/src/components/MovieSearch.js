import React, { useState } from "react";

const MovieSearch = ({ setMovieData, setError }) => {
    const [searchQuery, setSearchQuery] = useState("");

    const handleSearch = async (event) => {
        event.preventDefault();
        setError(null);
        setMovieData(null);

        try {
            const response = await fetch(`http://localhost:8000/movies/${searchQuery}`);
            const data = await response.json();

            if (data.error) {
                setError("Movie not found");
            } else {
                setMovieData(data);
            }
        } catch (err) {
            setError("Error fetching movie data");
        }
    };

    return (
        <div>
            <h1>🎬 Movie Search</h1>
            <form onSubmit={handleSearch} className="search-form">
                <input
                    type="text"
                    placeholder="Enter movie title..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="search-input"
                />
                <button type="submit" className="search-button">🔍 Search</button>
            </form>
        </div>
    );
};

export default MovieSearch;
