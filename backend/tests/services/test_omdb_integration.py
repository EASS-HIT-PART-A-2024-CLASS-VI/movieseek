import os
from app.services.omdb_service import fetch_movie_by_title

def test_fetch_movie_by_title_real_api():
    # Ensure your environment has a valid API key
    api_key = os.getenv("API_KEY")
    assert api_key, "API_KEY is not set in the environment."

    # Call the function with a real movie title
    result = fetch_movie_by_title("Inception")

    # Assert the structure of the result
    assert result["name"] == "Inception"
    assert result["year"] == "2010"
    assert "description" in result  # Ensure the description key exists
    assert "poster" in result       # Ensure the poster key exists
