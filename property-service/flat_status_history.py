from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Database setup
DATABASE_URL = "postgresql://username:password@localhost:5432/yourdatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the FlatStatusHistory model (based on property.sql schema)
class FlatStatusHistory(Base):
    __tablename__ = "flat_status_history"
    id = Column(Integer, primary_key=True, index=True)
    flat_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Operations

# Create a new flat status history
@app.post("/flat_status_history/", response_model=dict)
def create_flat_status_history(flat_status: dict, db: Session = Depends(get_db)):
    new_status = FlatStatusHistory(**flat_status)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return {"message": "Flat status history created successfully", "data": new_status}

# Read all flat status histories
@app.get("/flat_status_history/", response_model=list)
def get_flat_status_histories(db: Session = Depends(get_db)):
    return db.query(FlatStatusHistory).all()

# Read a specific flat status history by ID
@app.get("/flat_status_history/{id}", response_model=dict)
def get_flat_status_history(id: int, db: Session = Depends(get_db)):
    status = db.query(FlatStatusHistory).filter(FlatStatusHistory.id == id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Flat status history not found")
    return status

# Update a flat status history
@app.put("/flat_status_history/{id}", response_model=dict)
def update_flat_status_history(id: int, updated_data: dict, db: Session = Depends(get_db)):
    status = db.query(FlatStatusHistory).filter(FlatStatusHistory.id == id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Flat status history not found")
    for key, value in updated_data.items():
        setattr(status, key, value)
    db.commit()
    db.refresh(status)
    return {"message": "Flat status history updated successfully", "data": status}

# Delete a flat status history
@app.delete("/flat_status_history/{id}", response_model=dict)
def delete_flat_status_history(id: int, db: Session = Depends(get_db)):
    status = db.query(FlatStatusHistory).filter(FlatStatusHistory.id == id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Flat status history not found")
    db.delete(status)
    db.commit()
    return {"message": "Flat status history deleted successfully"}