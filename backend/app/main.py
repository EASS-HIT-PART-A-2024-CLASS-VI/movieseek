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

# OMDB Microservice URL
OMDB_SERVICE_URL = "http://omdb_service:8001/search"

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
    Fetches movie details from the OMDB Microservice.
    """
    response = requests.get(OMDB_SERVICE_URL, params={"title": title})  # Use "title" instead of "query"

    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail="Error fetching movie details")


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
