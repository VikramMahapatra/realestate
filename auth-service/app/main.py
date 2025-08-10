
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from common.db import Base, engine, SessionLocal
from . import models, schemas, crud, auth
from fastapi.security import OAuth2PasswordRequestForm

# create tables (for demo only)
Base.metadata.create_all(bind=engine)

app = FastAPI(title='auth-service')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/register', response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate):
    db = SessionLocal()
    user = crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail='Email already registered')
    created = crud.create_user(db, user_in)
    db.close()
    return created

@app.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    db.close()
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    token = create_access_token(subject=str(user.id), role=user.role)
    return {{'access_token': token, 'token_type':'bearer'}}

@app.get('/me', response_model=schemas.UserOut)
def me(current = Depends(auth.get_current_user)):
    return current

@app.get('/admin-only')
def admin_only(current = Depends(auth.require_role('admin'))):
    return {{'msg':'hello admin', 'user': current.email}}
