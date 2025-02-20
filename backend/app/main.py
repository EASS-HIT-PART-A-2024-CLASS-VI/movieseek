from fastapi import FastAPI, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
import jwt
import requests
from contextlib import asynccontextmanager

from app.middlewares import add_cors_middleware
from app.schemas import UserLogin, UserRegistration
from app.dependencies import get_db
from app.services.user_service import register_user, fetch_registered_users, login_user
from app.database import Base, engine

# ✅ Update: TMDB Microservice URLs
TMDB_SEARCH_URL = "http://tmdb_service:8001/search"
TMDB_TRENDING_URL = "http://tmdb_service:8001/trending"
TMDB_TOP_RATED_URL = "http://tmdb_service:8001/top-rated"  # ✅ New: Fetch Top Rated Movies

# Secret key (must match the one in `user_service.py`)
SECRET_KEY = "your_secret_key"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown.
    """
    print("🚀 Starting up: Initializing Database")
    Base.metadata.create_all(bind=engine)  # Ensure DB tables exist

    yield  # Wait here until shutdown

    print("🛑 Shutting down: Cleaning up resources")  # Optional cleanup step


# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Apply CORS middleware
add_cors_middleware(app)


def verify_token(request: Request):
    """
    Middleware function to check if the JWT token from the cookie is valid.
    """
    token = request.cookies.get("access_token")  # Get JWT token from cookie
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # Token is valid, return user data
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
    Registers a new user.
    """
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
    """
    response = requests.get(TMDB_SEARCH_URL, params={"title": title})

    if response.status_code == 200:
        return response.json()
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
