from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection
DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

# FastAPI app
app = FastAPI()

# Pydantic model for property
class Property(BaseModel):
    id: int
    name: str
    location: str
    price: float

# Create
@app.post("/properties/", response_model=Property)
def create_property(property: Property):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO properties (id, name, location, price) VALUES (%s, %s, %s, %s) RETURNING *",
            (property.id, property.name, property.location, property.price),
        )
        new_property = cursor.fetchone()
        conn.commit()
        return new_property
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Read all
@app.get("/properties/", response_model=List[Property])
def get_properties():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM properties")
        properties = cursor.fetchall()
        return properties
    finally:
        cursor.close()
        conn.close()

# Read one
@app.get("/properties/{property_id}", response_model=Property)
def get_property(property_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM properties WHERE id = %s", (property_id,))
        property = cursor.fetchone()
        if property is None:
            raise HTTPException(status_code=404, detail="Property not found")
        return property
    finally:
        cursor.close()
        conn.close()

# Update
@app.put("/properties/{property_id}", response_model=Property)
def update_property(property_id: int, property: Property):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE properties SET name = %s, location = %s, price = %s WHERE id = %s RETURNING *",
            (property.name, property.location, property.price, property_id),
        )
        updated_property = cursor.fetchone()
        if updated_property is None:
            raise HTTPException(status_code=404, detail="Property not found")
        conn.commit()
        return updated_property
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Delete
@app.delete("/properties/{property_id}", response_model=dict)
def delete_property(property_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM properties WHERE id = %s RETURNING id", (property_id,))
        deleted_property = cursor.fetchone()
        if deleted_property is None:
            raise HTTPException(status_code=404, detail="Property not found")
        conn.commit()
        return {"message": "Property deleted successfully"}
    finally:
        cursor.close()
        conn.close()