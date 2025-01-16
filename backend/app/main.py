# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import Base, engine, SessionLocal
from app.models import RegisteredUser
from app.omdb_service import fetch_movie_by_title

app = FastAPI()

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# 2. Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

# 3. Register a user (new endpoint)
@app.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    """
    Register a new user with a username and password.
    Passwords are hashed before being stored.
    """
    # Check if the username already exists
    existing_user = db.query(RegisteredUser).filter(RegisteredUser.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password before storing it
    hashed_password = pwd_context.hash(password)

    # Create and store the user
    new_user = RegisteredUser(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "username": new_user.username}

# 4. Fetch all registered users (renamed from /users for clarity)
@app.get("/registered-users")
def fetch_registered_users(db: Session = Depends(get_db)):
    """
    Fetch all registered users (excluding their passwords).
    """
    users = db.query(RegisteredUser).all()
    return [{"id": user.id, "username": user.username} for user in users]

# 5. Example OMDb endpoint
@app.get("/movies/{title}")
def get_movie(title: str):
    movie_data = fetch_movie_by_title(title)
    return movie_data
