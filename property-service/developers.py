from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import IntegrityError

# Database setup
DATABASE_URL = "postgresql://username:password@localhost:5432/property"  # Replace with your PostgreSQL credentials
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the developers table
class Developer(Base):
    __tablename__ = "developers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

Base.metadata.create_all(bind=engine)

# Pydantic models
class DeveloperCreate(BaseModel):
    name: str
    email: EmailStr

class DeveloperResponse(DeveloperCreate):
    id: int

    class Config:
        orm_mode = True

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI()

@app.post("/developers/", response_model=DeveloperResponse)
def create_developer(developer: DeveloperCreate, db: Session = Depends(get_db)):
    db_developer = Developer(name=developer.name, email=developer.email)
    try:
        db.add(db_developer)
        db.commit()
        db.refresh(db_developer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    return db_developer

@app.get("/developers/", response_model=List[DeveloperResponse])
def read_developers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Developer).offset(skip).limit(limit).all()

@app.get("/developers/{developer_id}", response_model=DeveloperResponse)
def read_developer(developer_id: int, db: Session = Depends(get_db)):
    developer = db.query(Developer).filter(Developer.id == developer_id).first()
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    return developer

@app.put("/developers/{developer_id}", response_model=DeveloperResponse)
def update_developer(developer_id: int, developer: DeveloperCreate, db: Session = Depends(get_db)):
    db_developer = db.query(Developer).filter(Developer.id == developer_id).first()
    if not db_developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    db_developer.name = developer.name
    db_developer.email = developer.email
    try:
        db.commit()
        db.refresh(db_developer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    return db_developer

@app.delete("/developers/{developer_id}")
def delete_developer(developer_id: int, db: Session = Depends(get_db)):
    db_developer = db.query(Developer).filter(Developer.id == developer_id).first()
    if not db_developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    db.delete(db_developer)
    db.commit()
    return {"detail": "Developer deleted successfully"}