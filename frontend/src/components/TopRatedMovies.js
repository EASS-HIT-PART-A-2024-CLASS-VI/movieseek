import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const TopRatedMovies = () => {
    const [topRatedMovies, setTopRatedMovies] = useState([]);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1); // ✅ Default page is 1
    const navigate = useNavigate();

    useEffect(() => {
        fetchTopRatedMovies(currentPage); // ✅ Fetch the selected page on load or change
    }, [currentPage]);

    const fetchTopRatedMovies = async (page) => {
        try {
            const response = await fetch(`http://localhost:8000/top-rated-movies?page=${page}`);
            const data = await response.json();

            if (data.detail) {
                setError("Error fetching top-rated movies");
            } else {
                setTopRatedMovies(data);
            }
        } catch (err) {
            setError("Error fetching top-rated movies");
        }
    };

    // ✅ Function to change page when a number is clicked
    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    // ✅ Function to handle clicking on a movie
    const handleMovieClick = (movieName) => {
        navigate(`/movie/${movieName}`);
    };

    return (
        <div>
            <h2>⭐ Top Rated Movies</h2>
            {error && <p className="error-message">{error}</p>}

            <div className="top-rated-movies">
                {topRatedMovies.map((movie, index) => (
                    <div 
                        key={index} 
                        className="movie-card"
                        onClick={() => handleMovieClick(movie.name)}
                        style={{ cursor: "pointer" }}
                    >
                        <img src={movie.poster} alt={movie.name} className="movie-thumbnail" />
                        <h3>{movie.name}</h3>
                    </div>
                ))}
            </div>

            {/* ✅ Pagination buttons */}
            <div className="pagination">
                {Array.from({ length: 10 }, (_, i) => i + 1).map((page) => (
                    <button
                        key={page}
                        className={`page-button ${currentPage === page ? "active" : ""}`}
                        onClick={() => handlePageChange(page)}
                    >
                        {page}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default TopRatedMovies;
