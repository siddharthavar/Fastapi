from fastapi import FastAPI
from .database import engine
from .routers import user, post, auth, vote
from .import models
from .config import settings
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware

print(settings)
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional, List
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session


#user for giving instruction  to the database for creating table if not present
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins=["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return  p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"]== id:
#             return i
        

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}