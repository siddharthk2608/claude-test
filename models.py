from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class User(BaseModel):
    username: str
    email: str
    role: Role
    disabled: Optional[bool] = False


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[Role] = None


class UserLogin(BaseModel):
    username: str
    password: str
