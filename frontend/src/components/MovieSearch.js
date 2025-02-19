import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ Import useNavigate

const MovieSearch = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const navigate = useNavigate(); // ✅ Hook for navigation

    const handleSearch = async (event) => {
        event.preventDefault();
        if (!searchQuery.trim()) return; // Prevent empty search
        
        navigate(`/movie/${searchQuery}`); // ✅ Navigate to the movie page
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
