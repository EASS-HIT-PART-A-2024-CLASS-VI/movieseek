from fastapi import FastAPI, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
import jwt
import requests
from contextlib import asynccontextmanager

from app.middlewares import add_cors_middleware
from app.schemas import UserLogin, UserRegistration, SavedMovieSchema
from app.dependencies import get_db
from app.services.user_service import register_user, fetch_registered_users, login_user
from app.services.movie_service import save_movie, get_saved_movies, remove_saved_movie
from app.database import Base, engine
from app.models import RegisteredUser  # ✅ Fix: Import RegisteredUser

# ✅ Update: TMDB Microservice URLs
TMDB_SEARCH_URL = "http://tmdb_service:8001/search"
TMDB_TRENDING_URL = "http://tmdb_service:8001/trending"
TMDB_TOP_RATED_URL = "http://tmdb_service:8001/top-rated"  # ✅ Fetch Top Rated Movies

# Secret key (must match the one in `user_service.py`)
SECRET_KEY = "your_secret_key"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up: Initializing Database")
    Base.metadata.create_all(bind=engine)  # Ensure DB tables exist
    yield
    print("🛑 Shutting down: Cleaning up resources")

app = FastAPI(lifespan=lifespan)
add_cors_middleware(app)

def verify_token(request: Request, db: Session = Depends(get_db)):
    """
    Middleware function to check if the JWT token from the cookie is valid.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if "username" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        # ✅ Fetch user from DB to get `id`
        user = db.query(RegisteredUser).filter(RegisteredUser.username == payload["username"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return {"id": user.id, "username": user.username}  # ✅ Return ID & username

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/")
def login_endpoint(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    """
    Logs a user in and stores the JWT token in an HttpOnly cookie.
    """
    return login_user(credentials.username, credentials.password, db, response)

@app.post("/register")
def register_user_endpoint(user: UserRegistration, db: Session = Depends(get_db)):
    """
    Registers a new user with validation.
    """
    if not user.username.strip() or not user.password.strip():
        raise HTTPException(status_code=400, detail="Username and password cannot be empty.")

    return register_user(user.username, user.password, db)

@app.get("/registered-users")
def get_registered_users(db: Session = Depends(get_db)):
    """
    Fetches all registered users.
    """
    return fetch_registered_users(db)

@app.get("/movies/{title}")
def get_movie(title: str):
    """
    ✅ Fetch movie details from the TMDB Microservice.
    Includes genres and trailer.
    """
    response = requests.get(TMDB_SEARCH_URL, params={"title": title})

    if response.status_code == 200:
        movie_data = response.json()
        return {
            "name": movie_data.get("name"),
            "year": movie_data.get("year"),
            "description": movie_data.get("description"),
            "poster": movie_data.get("poster"),
            "genres": movie_data.get("genres", []),  # ✅ Include genres
            "trailer": movie_data.get("trailer")  # ✅ Include trailer
        }

    raise HTTPException(status_code=response.status_code, detail="Error fetching movie details")

@app.get("/trending-movies")
def get_trending_movies():
    """
    ✅ Fetch trending movies from the TMDB Microservice.
    """
    response = requests.get(TMDB_TRENDING_URL)  # Fetch trending movies

    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail="Error fetching trending movies")

@app.get("/top-rated-movies")
def get_top_rated_movies(page: int = 1):  # ✅ Accept page number
    """
    Fetch top-rated movies from the TMDB Microservice with pagination.
    """
    response = requests.get(f"{TMDB_TOP_RATED_URL}?page={page}")  # ✅ Fetch the selected page

    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail="Error fetching top-rated movies")

@app.get("/protected")
def protected_route(user: dict = Depends(verify_token)):
    """
    Protected route that only authenticated users can access.
    """
    return {"message": f"Hello, {user['username']}! You are authenticated."}

@app.post("/logout")
def logout(response: Response):
    """
    Logs the user out by removing the JWT cookie.
    """
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

# ✅ NEW: Save a Movie
@app.post("/save-movie")
def save_movie_endpoint(movie: SavedMovieSchema, user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """
    ✅ Save a movie for the authenticated user.
    """
    return save_movie(user["id"], movie, db)

# ✅ NEW: Fetch Saved Movies
@app.get("/saved-movies")
def get_saved_movies_endpoint(user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """
    ✅ Fetch all saved movies for the authenticated user.
    """
    return get_saved_movies(user["id"], db)

# ✅ NEW: Remove a Saved Movie
@app.delete("/remove-movie/{movie_name}")
def remove_saved_movie_endpoint(movie_name: str, user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """
    ✅ Remove a saved movie from the user's account.
    """
    return remove_saved_movie(user["id"], movie_name, db)
