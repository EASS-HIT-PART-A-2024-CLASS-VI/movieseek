from fastapi import FastAPI, HTTPException 
from tmdb_service import fetch_movie_by_title, fetch_trending_movies, fetch_top_rated_movies

app = FastAPI()

@app.get("/search")
async def search_movie(title: str):
    """
    Fetch movie details from the TMDB API via the microservice.
    Now includes genres and trailer.
    """
    result = fetch_movie_by_title(title)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/trending")
async def trending_movies():
    """
    Fetch 20 trending movies from TMDB API.
    """
    result = fetch_trending_movies()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.get("/top-rated")
async def top_rated_movies(page: int = 1):  # ✅ Accept page number from frontend/backend
    """
    Fetch 20 top-rated movies from TMDB API with pagination.
    """
    result = fetch_top_rated_movies(page)  # ✅ Call the function with page number
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
