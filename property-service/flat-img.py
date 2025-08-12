from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection
DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")

# FastAPI app
app = FastAPI()

# Pydantic model
class FlatImage(BaseModel):
    id: int = None
    property_id: int
    image_url: str

# CRUD Operations

@app.post("/flat-images/", response_model=FlatImage)
def create_flat_image(flat_image: FlatImage):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO flat_images (property_id, image_url) VALUES (%s, %s) RETURNING id, property_id, image_url",
            (flat_image.property_id, flat_image.image_url),
        )
        result = cursor.fetchone()
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Failed to create flat image")
    finally:
        cursor.close()
        conn.close()

@app.get("/flat-images/", response_model=List[FlatImage])
def get_all_flat_images():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM flat_images")
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to fetch flat images")
    finally:
        cursor.close()
        conn.close()

@app.get("/flat-images/{image_id}", response_model=FlatImage)
def get_flat_image(image_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM flat_images WHERE id = %s", (image_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Flat image not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to fetch flat image")
    finally:
        cursor.close()
        conn.close()

@app.put("/flat-images/{image_id}", response_model=FlatImage)
def update_flat_image(image_id: int, flat_image: FlatImage):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE flat_images SET property_id = %s, image_url = %s WHERE id = %s RETURNING id, property_id, image_url",
            (flat_image.property_id, flat_image.image_url, image_id),
        )
        result = cursor.fetchone()
        conn.commit()
        if not result:
            raise HTTPException(status_code=404, detail="Flat image not found")
        return result
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Failed to update flat image")
    finally:
        cursor.close()
        conn.close()

@app.delete("/flat-images/{image_id}")
def delete_flat_image(image_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM flat_images WHERE id = %s RETURNING id", (image_id,))
        result = cursor.fetchone()
        conn.commit()
        if not result:
            raise HTTPException(status_code=404, detail="Flat image not found")
        return {"message": "Flat image deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Failed to delete flat image")
    finally:
        cursor.close()
        conn.close()