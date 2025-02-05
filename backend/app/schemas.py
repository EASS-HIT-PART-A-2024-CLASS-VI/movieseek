from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegistration(BaseModel):
    username: str
    password: str
