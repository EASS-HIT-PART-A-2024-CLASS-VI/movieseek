from fastapi import FastAPI, HTTPException
import os
from omdb_service import fetch_movie_by_title  # Import the function correctly

app = FastAPI()

@app.get("/search")
async def search_movie(title: str):
    """
    Fetch movie details from the OMDB API via the microservice.
    """
    result = fetch_movie_by_title(title)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
