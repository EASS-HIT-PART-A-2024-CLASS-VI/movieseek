# models.py

from sqlalchemy import Column, Integer, String
from app.database import Base

class DemoUser(Base):
    __tablename__ = "demo_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)  # Unique usernames
    hashed_password = Column(String(200), nullable=False)         # Store hashed passwords
