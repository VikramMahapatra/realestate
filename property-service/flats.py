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
        host="localhost",
        port="5432"
    )

# FastAPI app
app = FastAPI()

# Pydantic model for Flats
class Flat(BaseModel):
    id: int = None
    name: str
    location: str
    price: float

# Create a flat
@app.post("/flats/", response_model=Flat)
def create_flat(flat: Flat):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "INSERT INTO flats (name, location, price) VALUES (%s, %s, %s) RETURNING *",
            (flat.name, flat.location, flat.price)
        )
        new_flat = cursor.fetchone()
        conn.commit()
        return new_flat
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Read all flats
@app.get("/flats/", response_model=List[Flat])
def get_flats():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM flats")
        flats = cursor.fetchall()
        return flats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Read a single flat by ID
@app.get("/flats/{flat_id}", response_model=Flat)
def get_flat(flat_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM flats WHERE id = %s", (flat_id,))
        flat = cursor.fetchone()
        if not flat:
            raise HTTPException(status_code=404, detail="Flat not found")
        return flat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Update a flat
@app.put("/flats/{flat_id}", response_model=Flat)
def update_flat(flat_id: int, flat: Flat):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "UPDATE flats SET name = %s, location = %s, price = %s WHERE id = %s RETURNING *",
            (flat.name, flat.location, flat.price, flat_id)
        )
        updated_flat = cursor.fetchone()
        if not updated_flat:
            raise HTTPException(status_code=404, detail="Flat not found")
        conn.commit()
        return updated_flat
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Delete a flat
@app.delete("/flats/{flat_id}")
def delete_flat(flat_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM flats WHERE id = %s RETURNING id", (flat_id,))
        deleted_flat = cursor.fetchone()
        if not deleted_flat:
            raise HTTPException(status_code=404, detail="Flat not found")
        conn.commit()
        return {"message": "Flat deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()