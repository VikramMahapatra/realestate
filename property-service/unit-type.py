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

# Pydantic model for unit_types
class UnitType(BaseModel):
    id: int
    name: str
    description: str

# Dependency to get database connection
def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

# Create
@app.post("/unit-types/", response_model=UnitType)
def create_unit_type(unit_type: UnitType, db: Session = Depends(get_db)):
    query = "INSERT INTO unit_types (id, name, description) VALUES (%s, %s, %s) RETURNING *"
    with db.cursor() as cursor:
        cursor.execute(query, (unit_type.id, unit_type.name, unit_type.description))
        db.commit()
        result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create unit type")
    return result

# Read all
@app.get("/unit-types/", response_model=List[UnitType])
def get_all_unit_types(db: Session = Depends(get_db)):
    query = "SELECT * FROM unit_types"
    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

# Read by ID
@app.get("/unit-types/{unit_type_id}", response_model=UnitType)
def get_unit_type(unit_type_id: int, db: Session = Depends(get_db)):
    query = "SELECT * FROM unit_types WHERE id = %s"
    with db.cursor() as cursor:
        cursor.execute(query, (unit_type_id,))
        result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Unit type not found")
    return result

# Update
@app.put("/unit-types/{unit_type_id}", response_model=UnitType)
def update_unit_type(unit_type_id: int, unit_type: UnitType, db: Session = Depends(get_db)):
    query = "UPDATE unit_types SET name = %s, description = %s WHERE id = %s RETURNING *"
    with db.cursor() as cursor:
        cursor.execute(query, (unit_type.name, unit_type.description, unit_type_id))
        db.commit()
        result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Unit type not found")
    return result

# Delete
@app.delete("/unit-types/{unit_type_id}")
def delete_unit_type(unit_type_id: int, db: Session = Depends(get_db)):
    query = "DELETE FROM unit_types WHERE id = %s RETURNING id"
    with db.cursor() as cursor:
        cursor.execute(query, (unit_type_id,))
        db.commit()
        result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Unit type not found")
    return {"message": "Unit type deleted successfully"}