# user_service.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import RegisteredUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def login_user(username: str, password: str, db: Session):
    """
    Validate if a user's username and password match the database record.
    """
    user = db.query(RegisteredUser).filter(RegisteredUser.username == username).first()
    if not user:
        # 400 or 404 would both make sense; 404 (Not Found) might be more semantically correct
        raise HTTPException(status_code=404, detail="User does not exist.")

    # Verify hashed password
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password.")

    return {"message": "Login successful"}

def fetch_registered_users(db: Session):
    """
    Fetch all registered users (excluding their passwords).
    """
    users = db.query(RegisteredUser).all()
    return [{"id": user.id, "username": user.username} for user in users]
