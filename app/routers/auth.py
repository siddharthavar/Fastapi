from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database , schemas, models, utils, oauth2
router= APIRouter(tags=["authentication"])

@router.post("/login", response_model=schemas.Token)
def login( user_cred: OAuth2PasswordRequestForm = Depends() ,db:Session =Depends(database.get_db)):

    user=db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"invalid cred")
    
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"invalid cred")
#creation of token and return of token
    access_token= oauth2.create_accrss_token(data ={"user_id": user.id})


    return {"token": access_token , "token_type": "Bearer"} 