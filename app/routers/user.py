from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from ..import models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["users"]
)



#creating a new user
@router.post( "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Userout )
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    #hash th pass which can be retrived 
     hashed_password=utils.hash(user.password)
     user.password= hashed_password
     new_user=models.User(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return  new_user

@router.get("/{id}", response_model=schemas.Userout)
def get_user(id: int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} is not found")
    return user