from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="your_db_name",
        user="your_db_user",
        password="your_db_password",
        host="your_db_host",
        port="your_db_port"
    )

# Pydantic model for property
class Property(BaseModel):
    id: int = None
    name: str
    location: str
    price: float

app = FastAPI()

# Create
@app.post("/properties/", response_model=Property)
def create_property(property: Property):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO properties (name, location, price) VALUES (%s, %s, %s) RETURNING id;",
            (property.name, property.location, property.price)
        )
        property_id = cursor.fetchone()[0]
        conn.commit()
        property.id = property_id
        return property
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Read all
@app.get("/properties/", response_model=List[Property])
def get_properties():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM properties;")
        properties = cursor.fetchall()
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Read one
@app.get("/properties/{property_id}", response_model=Property)
def get_property(property_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM properties WHERE id = %s;", (property_id,))
        property = cursor.fetchone()
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        return property
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
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
            "UPDATE properties SET name = %s, location = %s, price = %s WHERE id = %s;",
            (property.name, property.location, property.price, property_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Property not found")
        conn.commit()
        property.id = property_id
        return property
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Delete
@app.delete("/properties/{property_id}")
def delete_property(property_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM properties WHERE id = %s;", (property_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Property not found")
        conn.commit()
        return {"message": "Property deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()