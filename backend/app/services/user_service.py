import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from app.models import RegisteredUser

SECRET_KEY = "your_secret_key"

def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a bcrypt hash.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_jwt_token(user: dict, expires_delta: int = 60):
    """
    Creates a JWT token with an expiration time.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    data = {"id": user["id"], "username": user["username"], "exp": expire}  # ✅ Include `id`
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def register_user(username: str, password: str, db: Session):
    """
    Register a new user with a username and password.
    """
    existing_user = db.query(RegisteredUser).filter(RegisteredUser.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = hash_password(password)
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

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password.")

    # ✅ Generate JWT token with `id` and `username`
    token = create_jwt_token({"id": user.id, "username": user.username})

    # ✅ Set JWT token in an HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="Lax",
        secure=False  # Set to True in production (requires HTTPS)
    )

    return {"message": "Login successful"}


def fetch_registered_users(db: Session):
    """
    Fetch all registered users (excluding their passwords).
    """
    users = db.query(RegisteredUser).all()
    return [{"id": user.id, "username": user.username} for user in users]
