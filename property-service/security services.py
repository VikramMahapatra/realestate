from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

DATABASE_URL = "postgresql+asyncpg://username:password@localhost/property_db"

# Database setup
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Define the Property model
class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

# Pydantic schema for request/response
class PropertyCreate(BaseModel):
    name: str
    location: str
    price: int

class PropertyResponse(PropertyCreate):
    id: int

    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Uncomment the line below if you want to create tables automatically
        # await conn.run_sync(Base.metadata.create_all)
        pass

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

# Create a new property
@app.post("/properties/", response_model=PropertyResponse)
async def create_property(property: PropertyCreate):
    async with async_session() as session:
        new_property = Property(**property.dict())
        session.add(new_property)
        await session.commit()
        await session.refresh(new_property)
        return new_property

# Get a property by ID
@app.get("/properties/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: int):
    async with async_session() as session:
        property = await session.get(Property, property_id)
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        return property

# Update a property
@app.put("/properties/{property_id}", response_model=PropertyResponse)
async def update_property(property_id: int, property: PropertyCreate):
    async with async_session() as session:
        existing_property = await session.get(Property, property_id)
        if not existing_property:
            raise HTTPException(status_code=404, detail="Property not found")
        for key, value in property.dict().items():
            setattr(existing_property, key, value)
        await session.commit()
        await session.refresh(existing_property)
        return existing_property

# Delete a property
@app.delete("/properties/{property_id}")
async def delete_property(property_id: int):
    async with async_session() as session:
        property = await session.get(Property, property_id)
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        await session.delete(property)
        await session.commit()
        return {"message": "Property deleted successfully"}