from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime

# Database setup
DATABASE_URL = "postgresql://username:password@localhost:5432/yourdatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the table structure (should match your propertey.sql)
class PropertyStatusHistory(Base):
    __tablename__ = "property_status_history"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Pydantic models
class PropertyStatusHistoryCreate(BaseModel):
    property_id: int
    status: str

class PropertyStatusHistoryResponse(PropertyStatusHistoryCreate):
    id: int
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

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
@app.post("/properties-status-history/", response_model=PropertyStatusHistoryResponse)
def create_property_status_history(
    property_status: PropertyStatusHistoryCreate, db: Session = Depends(get_db)
):
    db_property_status = PropertyStatusHistory(**property_status.dict())
    db.add(db_property_status)
    db.commit()
    db.refresh(db_property_status)
    return db_property_status

@app.get("/properties-status-history/{id}", response_model=PropertyStatusHistoryResponse)
def read_property_status_history(id: int, db: Session = Depends(get_db)):
    db_property_status = db.query(PropertyStatusHistory).filter(PropertyStatusHistory.id == id).first()
    if not db_property_status:
        raise HTTPException(status_code=404, detail="Property status history not found")
    return db_property_status

@app.put("/properties-status-history/{id}", response_model=PropertyStatusHistoryResponse)
def update_property_status_history(
    id: int, property_status: PropertyStatusHistoryCreate, db: Session = Depends(get_db)
):
    db_property_status = db.query(PropertyStatusHistory).filter(PropertyStatusHistory.id == id).first()
    if not db_property_status:
        raise HTTPException(status_code=404, detail="Property status history not found")
    for key, value in property_status.dict().items():
        setattr(db_property_status, key, value)
    db.commit()
    db.refresh(db_property_status)
    return db_property_status

@app.delete("/properties-status-history/{id}")
def delete_property_status_history(id: int, db: Session = Depends(get_db)):
    db_property_status = db.query(PropertyStatusHistory).filter(PropertyStatusHistory.id == id).first()
    if not db_property_status:
        raise HTTPException(status_code=404, detail="Property status history not found")
    db.delete(db_property_status)
    db.commit()
    return {"message": "Property status history deleted successfully"}