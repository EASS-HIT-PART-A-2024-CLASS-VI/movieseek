import os
from unittest.mock import patch
from app.services.omdb_service import fetch_movie_by_title

# Ensure the API key is retrieved from the environment
API_KEY = os.getenv("API_KEY")

def test_fetch_movie_by_title_success():
    # Mock the response from the OMDb API
    mock_response = {
        "Response": "True",
        "Title": "Inception",
        "Year": "2010",
        "Plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "Poster": "http://example.com/poster.jpg"
    }

    # Expected result based on the function's return structure
    expected_result = {
        "name": "Inception",
        "year": "2010",
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "poster": "http://example.com/poster.jpg"
    }

    with patch("app.services.omdb_service.requests.get") as mock_get:
        # Configure the mock to return a response with a .json() method
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Call the function and assert the result matches the mock
        result = fetch_movie_by_title("Inception")
        assert result == expected_result
        mock_get.assert_called_once_with(
            "http://www.omdbapi.com/",
            params={"apikey": API_KEY, "t": "Inception", "plot": "full"}
        )


def test_fetch_movie_by_title_not_found():
    # Mock response for a non-existent movie
    mock_response = {
        "Response": "False",
        "Error": "Movie not found!"
    }

    with patch("app.services.omdb_service.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Call the function and assert it returns an error message
        result = fetch_movie_by_title("Nonexistent Movie")
        assert result == {"error": "Movie not found"}
        mock_get.assert_called_once_with(
            "http://www.omdbapi.com/",
            params={"apikey": API_KEY, "t": "Nonexistent Movie", "plot": "full"}
        )


def test_fetch_movie_by_title_api_failure():
    with patch("app.services.omdb_service.requests.get") as mock_get:
        # Simulate an API failure (e.g., 500 Internal Server Error)
        mock_get.return_value.status_code = 500

        # Call the function and assert it returns an error message
        result = fetch_movie_by_title("Any Movie")
        assert result == {"error": "Failed to fetch data. Status code: 500"}
        mock_get.assert_called_once_with(
            "http://www.omdbapi.com/",
            params={"apikey": API_KEY, "t": "Any Movie", "plot": "full"}
        )

