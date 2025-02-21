from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class RegisteredUser(Base):
    __tablename__ = "registered_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)  # Unique usernames
    hashed_password = Column(String(200), nullable=False)         # Store hashed passwords

    # Relationship with saved movies
    saved_movies = relationship("SavedMovie", back_populates="user", cascade="all, delete")

class SavedMovie(Base):
    __tablename__ = "saved_movies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("registered_users.id", ondelete="CASCADE"))
    movie_name = Column(String(255), nullable=False)
    movie_year = Column(String(10), nullable=True)
    movie_description = Column(String(500), nullable=True)
    movie_poster = Column(String(255), nullable=True)

    user = relationship("RegisteredUser", back_populates="saved_movies")
