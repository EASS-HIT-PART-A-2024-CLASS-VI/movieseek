# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.services.user_service import register_user, fetch_registered_users, login_user
from app.services.omdb_service import fetch_movie_by_title


app = FastAPI()

# Pydantic model for Login
class UserLogin(BaseModel):
    username: str
    password: str

# Pydantic model for request body
class UserRegistration(BaseModel):
    username: str
    password: str

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)

@app.post("/")
def login_endpoint(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Logs a user in if their username and password match a record in the DB.
    Returns success if valid, raises HTTPException if invalid.
    """
    return login_user(credentials.username, credentials.password, db)


@app.post("/register")
def register_user_endpoint(user: UserRegistration, db: Session = Depends(get_db)):
    """
    This route function delegates user registration to user_service.
    """
    return register_user(user.username, user.password, db)


# Fetch all registered users
@app.get("/registered-users")
def get_registered_users(db: Session = Depends(get_db)):
    return fetch_registered_users(db)

# Movie endpoint
@app.get("/movies/{title}")
def get_movie(title: str):
    return fetch_movie_by_title(title)

