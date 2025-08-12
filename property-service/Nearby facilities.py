from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"  # Replace with your PostgreSQL credentials
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Property model
class Property(Base):
    __tablename__ = "property"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    price = Column(Float, nullable=False)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Pydantic models for request/response validation
class PropertyCreate(BaseModel):
    name: str
    address: str
    price: float

class PropertyResponse(PropertyCreate):
    id: int

    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
@app.post("/properties/", response_model=PropertyResponse)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    db_property = Property(name=property.name, address=property.address, price=property.price)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@app.get("/properties/", response_model=List[PropertyResponse])
def read_properties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Property).offset(skip).limit(limit).all()

@app.get("/properties/{property_id}", response_model=PropertyResponse)
def read_property(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property

@app.put("/properties/{property_id}", response_model=PropertyResponse)
def update_property(property_id: int, property: PropertyCreate, db: Session = Depends(get_db)):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    db_property.name = property.name
    db_property.address = property.address
    db_property.price = property.price
    db.commit()
    db.refresh(db_property)
    return db_property

@app.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(db_property)
    db.commit()
    return {"detail": "Property deleted successfully"}