from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Post(Base):
    __tablename__ ="posts"

    id=Column(Integer, primary_key = True, nullable = False)
    title= Column(String(100),nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default="True")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id=Column(Integer, primary_key = True, nullable = False)
    email= Column(String(256),unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey('users.id', ondelete="CASCADe"), primary_key=True)
    post_id = Column(Integer,ForeignKey('posts.id', ondelete="CASCADe"),primary_key=True)

