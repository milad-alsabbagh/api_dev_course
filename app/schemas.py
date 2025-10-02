
from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr
from pydantic.types import conint

class UserBase(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    published: bool = True

    class Config:
        orm_mode = True  # This allows the model to work with SQLAlchemy models
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at:datetime
    owner_id:int
    owner:UserResponse
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:Post
    votes:int




class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None

class Vote(BaseModel):
    post_id:int
    dir:int