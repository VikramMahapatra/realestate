from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the model based on property.sql
class FlatPricingHistory(Base):
    __tablename__ = "flat_pricing_history"
    id = Column(Integer, primary_key=True, index=True)
    flat_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(String, nullable=False)

# Pydantic schema
class FlatPricingHistoryCreate(BaseModel):
    flat_id: int
    price: float
    date: str

class FlatPricingHistoryResponse(FlatPricingHistoryCreate):
    id: int

    class Config:
        orm_mode = True

# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
@app.post("/flat_pricing_history/", response_model=FlatPricingHistoryResponse)
def create_flat_pricing_history(data: FlatPricingHistoryCreate, db: Session = Depends(get_db)):
    new_entry = FlatPricingHistory(**data.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@app.get("/flat_pricing_history/", response_model=List[FlatPricingHistoryResponse])
def read_flat_pricing_histories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(FlatPricingHistory).offset(skip).limit(limit).all()

@app.get("/flat_pricing_history/{id}", response_model=FlatPricingHistoryResponse)
def read_flat_pricing_history(id: int, db: Session = Depends(get_db)):
    entry = db.query(FlatPricingHistory).filter(FlatPricingHistory.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@app.put("/flat_pricing_history/{id}", response_model=FlatPricingHistoryResponse)
def update_flat_pricing_history(id: int, data: FlatPricingHistoryCreate, db: Session = Depends(get_db)):
    entry = db.query(FlatPricingHistory).filter(FlatPricingHistory.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    for key, value in data.dict().items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry

@app.delete("/flat_pricing_history/{id}")
def delete_flat_pricing_history(id: int, db: Session = Depends(get_db)):
    entry = db.query(FlatPricingHistory).filter(FlatPricingHistory.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return {"detail": "Entry deleted successfully"}