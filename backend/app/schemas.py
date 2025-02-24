from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)  # ✅ Updated for Pydantic V2
