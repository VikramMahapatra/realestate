from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"

app = FastAPI()

# Pydantic model for ParkingSlot
class ParkingSlot(BaseModel):
    id: int
    name: str
    location: str
    is_available: bool

# Database connection function
def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        yield conn
    finally:
        conn.close()

# Create a parking slot
@app.post("/parking_slots/", response_model=ParkingSlot)
def create_parking_slot(parking_slot: ParkingSlot, db: Session = Depends(get_db)):
    query = """
    INSERT INTO parking_slots (id, name, location, is_available)
    VALUES (%s, %s, %s, %s) RETURNING *;
    """
    with db.cursor() as cursor:
        cursor.execute(query, (parking_slot.id, parking_slot.name, parking_slot.location, parking_slot.is_available))
        db.commit()
        result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create parking slot")
    return result

# Read all parking slots
@app.get("/parking_slots/", response_model=List[ParkingSlot])
def get_parking_slots(db: Session = Depends(get_db)):
    query = "SELECT * FROM parking_slots;"
    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

# Read a single parking slot by ID
@app.get("/parking_slots/{slot_id}", response_model=ParkingSlot)
def get_parking_slot(slot_id: int, db: Session = Depends(get_db)):
    query = "SELECT * FROM parking_slots WHERE id = %s;"
    with db.cursor() as cursor:
        cursor.execute(query, (slot_id,))
        result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return result

# Update a parking slot
@app.put("/parking_slots/{slot_id}", response_model=ParkingSlot)
def update_parking_slot(slot_id: int, parking_slot: ParkingSlot, db: Session = Depends(get_db)):
    query = """
    UPDATE parking_slots
    SET name = %s, location = %s, is_available = %s
    WHERE id = %s RETURNING *;
    """
    with db.cursor() as cursor:
        cursor.execute(query, (parking_slot.name, parking_slot.location, parking_slot.is_available, slot_id))
        db.commit()
        result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return result

# Delete a parking slot
@app.delete("/parking_slots/{slot_id}")
def delete_parking_slot(slot_id: int, db: Session = Depends(get_db)):
    query = "DELETE FROM parking_slots WHERE id = %s RETURNING id;"
    with db.cursor() as cursor:
        cursor.execute(query, (slot_id,))
        db.commit()
        result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return {"message": f"Parking slot with ID {slot_id} deleted successfully"}