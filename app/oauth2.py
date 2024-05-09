from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import settings
Oath2_schema = OAuth2PasswordBearer(tokenUrl= "login")
#secret key
#Algorithm 
#Expriation time of atoken
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_accrss_token(data: dict):
    to_encode=data.copy()
    expire  = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update( {"exp": expire} )

    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str , cred_exception):
    try:

        payload=jwt.decode(token , SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        print(type(id))
        if not id:
            raise cred_exception
        token_data= schemas.TokenData(id=str(id))
    except JWTError as e:
        print(e)
        cred_exception
    except AssertionError as e:
        print(e)    
    
    return token_data

def get_current_user(token: str=  Depends(Oath2_schema), db: Session= Depends(database.get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate creds"
                                   , headers={"WWW-Authentication":"BARRERE"})
    
    token= verify_access_token(token, cred_exception)
    user= db.query(models.User).filter(models.User.id ==token.id).first()
    
    return user