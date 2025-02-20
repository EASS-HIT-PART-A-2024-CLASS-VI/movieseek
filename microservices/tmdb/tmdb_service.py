from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")  # Ensure TMDB API key is in .env
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_movie_by_title(title):
    """
    Fetch movie data from TMDB API by title.
    """
    search_url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": title, "include_adult": False}

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        if results:
            movie_id = results[0]["id"]
            return fetch_movie_details(movie_id)
        else:
            return {"error": "Movie not found"}
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

def fetch_movie_details(movie_id):
    """
    Fetch detailed movie data from TMDB API using movie ID.
    """
    details_url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}

    response = requests.get(details_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data.get("title"),
            "year": data.get("release_date", "")[:4],
            "description": data.get("overview"),
            "poster": IMAGE_BASE_URL + data["poster_path"] if data.get("poster_path") else None
        }
    else:
        return {"error": f"Failed to fetch movie details. Status code: {response.status_code}"}

def fetch_trending_movies():
    """
    Fetch 20 trending movies from TMDB API (default page 1).
    """
    trending_url = f"{BASE_URL}/trending/movie/day"
    params = {"api_key": API_KEY, "page": 1}  # Always fetch page 1, which contains 20 movies

    response = requests.get(trending_url, params=params)
    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])  # Get all 20 movies (TMDB's default page size)

        return [
            {
                "name": movie.get("title"),
                "year": movie.get("release_date", "")[:4],
                "description": movie.get("overview"),
                "poster": IMAGE_BASE_URL + movie["poster_path"] if movie.get("poster_path") else None
            }
            for movie in movies
        ]
    else:
        return {"error": f"Failed to fetch trending movies. Status code: {response.status_code}"}

def fetch_top_rated_movies(page=1):
    """
    Fetch 20 top-rated movies from TMDB API with pagination.
    """
    top_rated_url = f"{BASE_URL}/movie/top_rated"
    params = {"api_key": API_KEY, "page": page}  # ✅ Fetch specific page

    response = requests.get(top_rated_url, params=params)
    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])

        return [
            {
                "name": movie.get("title"),
                "year": movie.get("release_date", "")[:4],
                "description": movie.get("overview"),
                "poster": IMAGE_BASE_URL + movie["poster_path"] if movie.get("poster_path") else None
            }
            for movie in movies
        ]
    else:
        return {"error": f"Failed to fetch top-rated movies. Status code: {response.status_code}"}
