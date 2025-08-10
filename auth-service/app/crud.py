
from sqlalchemy.orm import Session
from . import models, schemas
from common.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email==email).first()

def create_user(db: Session, user_in: schemas.UserCreate, role: str = 'agent'):
    hashed = hash_password(user_in.password)
    db_user = models.User(email=user_in.email, hashed_password=hashed, full_name=user_in.full_name, role=role)
    db.add(db_user); db.commit(); db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
