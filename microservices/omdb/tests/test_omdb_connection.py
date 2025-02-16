import os
import requests
import pytest

OMDB_API_KEY = os.getenv("OMDB_API_KEY", "your_api_key_here")
OMDB_URL = "http://www.omdbapi.com/"

@pytest.mark.parametrize("movie_title, expected_status, expected_key", [
    ("Inception", 200, "Title"),       # ✅ Movie exists
    ("NonExistentMovieXYZ", 200, "Error"),  # ❌ Movie does not exist
])
def test_fetch_movie(movie_title, expected_status, expected_key):
    """
    Tests fetching a movie by title from the OMDB API.
    """
    response = requests.get(OMDB_URL, params={"apikey": OMDB_API_KEY, "t": movie_title})

    assert response.status_code == expected_status, f"Unexpected status code: {response.status_code}"
    data = response.json()

    assert expected_key in data, f"Expected '{expected_key}' in response, got: {data}"


def test_invalid_api_key():
    """
    Tests fetching a movie with an invalid API key.
    """
    response = requests.get(OMDB_URL, params={"apikey": "INVALID_KEY", "t": "Inception"})

    assert response.status_code == 401 or response.status_code == 200
    assert "Error" in response.json(), "Expected an error due to invalid API key."


def test_omdb_service_endpoint():
    """
    Tests the OMDB microservice itself by making a request to /search in the microservice.
    """
    MICRO_OMDB_SERVICE_URL = "http://omdb_service:8001/search"
    response = requests.get(MICRO_OMDB_SERVICE_URL, params={"title": "Inception"})

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert "name" in response.json(), "Expected movie name in response"
