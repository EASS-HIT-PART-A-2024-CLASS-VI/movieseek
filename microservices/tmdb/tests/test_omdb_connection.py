import os
import requests
import pytest

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "your_api_key_here")
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAILS_URL = "https://api.themoviedb.org/3/movie"

@pytest.mark.parametrize("movie_title, expected_status, expected_key", [
    ("Inception", 200, "results"),       # ✅ Movie exists
    ("NonExistentMovieXYZ", 200, "results"),  # ❌ Movie does not exist, but response is still valid
])
def test_fetch_movie(movie_title, expected_status, expected_key):
    """
    Tests fetching a movie by title from the TMDB API.
    """
    response = requests.get(TMDB_SEARCH_URL, params={"api_key": TMDB_API_KEY, "query": movie_title})

    assert response.status_code == expected_status, f"Unexpected status code: {response.status_code}"
    data = response.json()

    assert expected_key in data, f"Expected '{expected_key}' in response, got: {data}"


def test_invalid_api_key():
    """
    Tests fetching a movie with an invalid API key.
    """
    response = requests.get(TMDB_SEARCH_URL, params={"api_key": "INVALID_KEY", "query": "Inception"})

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    assert "status_message" in response.json(), "Expected 'status_message' in error response"


def test_tmdb_service_endpoint():
    """
    Tests the TMDB microservice itself by making a request to /search in the microservice.
    """
    MICRO_TMDB_SERVICE_URL = "http://tmdb_service:8001/search"
    response = requests.get(MICRO_TMDB_SERVICE_URL, params={"title": "Inception"})

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    json_response = response.json()
    
    assert "name" in json_response, "Expected 'name' in response"
    assert "year" in json_response, "Expected 'year' in response"
    assert "description" in json_response, "Expected 'description' in response"
    assert "poster" in json_response, "Expected 'poster' in response"
