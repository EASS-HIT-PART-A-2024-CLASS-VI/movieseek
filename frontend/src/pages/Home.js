import React, { useState } from "react";

const Home = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const [movieData, setMovieData] = useState(null);
    const [error, setError] = useState(null);

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
        <div className="container">
            <h1>Movie Search</h1>
            <form onSubmit={handleSearch}>
                <input
                    type="text"
                    placeholder="Enter movie title..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button type="submit">Search</button>
            </form>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {movieData && (
                <div className="movie-info">
                    <h2>{movieData.name} ({movieData.year})</h2>
                    <img src={movieData.poster} alt={movieData.name} style={{ width: "200px" }} />
                    <p>{movieData.description}</p>
                </div>
            )}
        </div>
    );
};

export default Home;
