import jwt
import datetime
from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import RegisteredUser

# Secret key for signing JWT tokens (CHANGE THIS in production)
SECRET_KEY = "your_secret_key"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_jwt_token(data: dict, expires_delta: int = 60):
    """
    Creates a JWT token with an expiration time.
    """
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def register_user(username: str, password: str, db: Session):
    """
    Register a new user with a username and password.
    Passwords are hashed before being stored.
    """
    existing_user = db.query(RegisteredUser).filter(RegisteredUser.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = pwd_context.hash(password)
    new_user = RegisteredUser(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "username": new_user.username}

def login_user(username: str, password: str, db: Session, response: Response):
    """
    Validates user login and sets a JWT token in an HttpOnly cookie.
    """
    user = db.query(RegisteredUser).filter(RegisteredUser.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist.")

    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password.")

    # Generate JWT token
    token = create_jwt_token({"username": user.username})

    # Set JWT token in an HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # Prevents JavaScript access
        samesite="Lax",  # Helps with CSRF protection
        secure=False  # Set to True in production (requires HTTPS)
    )

    return {"message": "Login successful"}

def fetch_registered_users(db: Session):
    """
    Fetch all registered users (excluding their passwords).
    """
    users = db.query(RegisteredUser).all()
    return [{"id": user.id, "username": user.username} for user in users]
