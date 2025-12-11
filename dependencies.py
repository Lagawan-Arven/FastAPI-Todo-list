from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from auth import secret_key,algorithm

from jose import jwt,JWTError

from database import SESSION
import database_models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

#================================
        #GET A DB CONNECTION
#================================ 
def use_session():
    session = SESSION()
    try:
        yield session
    finally:
        session.close()


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(use_session)):

    try:
        payload = jwt.decode(token,secret_key,algorithms=[algorithm])
        user_id = int(payload.get("id"))
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid token!")
    
    db_user = session.query(database_models.User).filter(database_models.User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    return db_user