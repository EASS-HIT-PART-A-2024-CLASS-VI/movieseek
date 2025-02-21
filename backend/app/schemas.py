from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegistration(BaseModel):
    username: str
    password: str

class SavedMovieSchema(BaseModel):
    movie_name: str
    movie_year: str | None = None
    movie_description: str | None = None
    movie_poster: str | None = None

    class Config:
        from_attributes = True  # ✅ Fix for Pydantic V2
