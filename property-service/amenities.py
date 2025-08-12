from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"

engine = create_engine(DATABASE_URL)

app = FastAPI()

# Pydantic model for Amenities
class Amenity(BaseModel):
    id: int = None
    name: str
    description: str = None

# Dependency to get DB connection
def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

# Create
@app.post("/amenities/", response_model=Amenity)
def create_amenity(amenity: Amenity, db: Session = Depends(get_db)):
    query = "INSERT INTO amenities (name, description) VALUES (%s, %s) RETURNING id, name, description"
    with db.cursor() as cursor:
        cursor.execute(query, (amenity.name, amenity.description))
        db.commit()
        result = cursor.fetchone()
    return result

# Read all
@app.get("/amenities/", response_model=List[Amenity])
def get_amenities(db: Session = Depends(get_db)):
    query = "SELECT id, name, description FROM amenities"
    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

# Read one
@app.get("/amenities/{amenity_id}", response_model=Amenity)
def get_amenity(amenity_id: int, db: Session = Depends(get_db)):
    query = "SELECT id, name, description FROM amenities WHERE id = %s"
    with db.cursor() as cursor:
        cursor.execute(query, (amenity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Amenity not found")
    return result

# Update
@app.put("/amenities/{amenity_id}", response_model=Amenity)
def update_amenity(amenity_id: int, amenity: Amenity, db: Session = Depends(get_db)):
    query = "UPDATE amenities SET name = %s, description = %s WHERE id = %s RETURNING id, name, description"
    with db.cursor() as cursor:
        cursor.execute(query, (amenity.name, amenity.description, amenity_id))
        db.commit()
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Amenity not found")
    return result

# Delete
@app.delete("/amenities/{amenity_id}")
def delete_amenity(amenity_id: int, db: Session = Depends(get_db)):
    query = "DELETE FROM amenities WHERE id = %s RETURNING id"
    with db.cursor() as cursor:
        cursor.execute(query, (amenity_id,))
        db.commit()
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Amenity not found")
    return {"message": "Amenity deleted successfully"}