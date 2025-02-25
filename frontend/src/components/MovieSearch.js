import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./MovieSearch.css"; // ✅ Import styling

const MovieSearch = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const navigate = useNavigate();

    const handleSearch = (event) => {
        event.preventDefault();
        if (!searchQuery.trim()) return;
        
        navigate(`/movie/${searchQuery}`);
    };

    return (
        <form onSubmit={handleSearch} className="search-form"> {/* ✅ Removed extra div */}
            <input
                type="text"
                placeholder="Enter movie title..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
            />
            <button type="submit" className="search-button">🐱 Seek</button>
        </form>
    );
};

export default MovieSearch;
