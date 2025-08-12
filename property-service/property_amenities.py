from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )

# Pydantic model for property_amenities
class PropertyAmenity(BaseModel):
    id: int
    name: str
    description: str

app = FastAPI()

# Create
@app.post("/property_amenities/", response_model=PropertyAmenity)
def create_property_amenity(amenity: PropertyAmenity):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO property_amenities (id, name, description) VALUES (%s, %s, %s) RETURNING id, name, description",
            (amenity.id, amenity.name, amenity.description)
        )
        conn.commit()
        result = cursor.fetchone()
        return result
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Read all
@app.get("/property_amenities/", response_model=List[PropertyAmenity])
def get_property_amenities():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM property_amenities")
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        conn.close()

# Read one
@app.get("/property_amenities/{amenity_id}", response_model=PropertyAmenity)
def get_property_amenity(amenity_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM property_amenities WHERE id = %s", (amenity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Amenity not found")
        return result
    finally:
        cursor.close()
        conn.close()

# Update
@app.put("/property_amenities/{amenity_id}", response_model=PropertyAmenity)
def update_property_amenity(amenity_id: int, amenity: PropertyAmenity):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE property_amenities SET name = %s, description = %s WHERE id = %s RETURNING id, name, description",
            (amenity.name, amenity.description, amenity_id)
        )
        conn.commit()
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Amenity not found")
        return result
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Delete
@app.delete("/property_amenities/{amenity_id}")
def delete_property_amenity(amenity_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM property_amenities WHERE id = %s RETURNING id", (amenity_id,))
        conn.commit()
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Amenity not found")
        return {"message": "Amenity deleted successfully"}
    finally:
        cursor.close()
        conn.close()