from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import SavedMovie, RegisteredUser
from app.schemas import SavedMovieSchema

def save_movie(user_id: int, movie: SavedMovieSchema, db: Session):
    """
    Saves a movie for the authenticated user.
    If the movie is already saved, it simply returns the existing movie.
    """

    # ✅ Check if the movie is already saved by this user
    existing_movie = db.query(SavedMovie).filter(
        SavedMovie.user_id == user_id,
        SavedMovie.movie_name == movie.movie_name
    ).first()

    if existing_movie:
        return existing_movie  # ✅ Simply return the already saved movie (no error)

    new_movie = SavedMovie(
        user_id=user_id,
        movie_name=movie.movie_name,
        movie_year=movie.movie_year,
        movie_description=movie.movie_description,
        movie_poster=movie.movie_poster
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

def get_saved_movies(user_id: int, db: Session):
    """
    Fetches all saved movies for the authenticated user.
    """
    return db.query(SavedMovie).filter(SavedMovie.user_id == user_id).all()

def remove_saved_movie(user_id: int, movie_name: str, db: Session):
    """
    Removes a saved movie from the user's account.
    """
    movie = db.query(SavedMovie).filter(SavedMovie.user_id == user_id, SavedMovie.movie_name == movie_name).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()
    return {"message": "Movie removed successfully"}
