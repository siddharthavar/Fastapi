from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

#user login schema 
class UserLogin(BaseModel):
     email: EmailStr
     password: str

class Token(BaseModel):
     token: str
     token_type: str

class TokenData(BaseModel):
     id: Optional[str] = None

class Userout(BaseModel):
     id: int
     email: EmailStr
     created_at: datetime
     class Config:
            # orm_mode = True
            from_attributes=True      
#post

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    created_at: datetime
    id:int
    user_id: int
    # owner: Userout
    class Config:
            orm_mode = True 
            # from_attributes=True

class PostOut(BaseModel):
     post: Post
     votes: int            
     class Config:
            # orm_mode = True 
            from_attributes=True

class CreateUser(BaseModel):
     email: EmailStr
     password: str


class Vote(BaseModel):
     post_id: int
     dir: conint(le=1)