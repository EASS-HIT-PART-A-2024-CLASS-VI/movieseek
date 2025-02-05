from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.middlewares import add_cors_middleware
from app.schemas import UserLogin, UserRegistration
from app.dependencies import get_db
from app.services.user_service import register_user, fetch_registered_users, login_user
from app.services.omdb_service import fetch_movie_by_title

app = FastAPI()

# Apply CORS middleware
add_cors_middleware(app)

@app.post("/")
def login_endpoint(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Logs a user in if their username and password match a record in the DB.
    """
    return login_user(credentials.username, credentials.password, db)

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
    Fetches movie details from the OMDB API.
    """
    return fetch_movie_by_title(title)

@app.on_event("startup")
def on_startup():
    """
    Initializes the database tables on application startup.
    """
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
