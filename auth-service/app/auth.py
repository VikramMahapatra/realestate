
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from common.security import create_access_token, decode_token
from common.db import SessionLocal
from . import models
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate':'Bearer'},
    )
    payload = decode_token(token)
    if not payload:
        raise credentials_exception
    user_id = payload.get('sub')
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.id==int(user_id)).first()
    finally:
        db.close()
    if not user:
        raise credentials_exception
    return user

def require_role(role: str):
    def _checker(current = Depends(get_current_user)):
        if current.role != role and current.role != 'admin':
            raise HTTPException(status_code=403, detail='Operation not permitted')
        return current
    return _checker
