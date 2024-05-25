from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
import httpx
from app.db.database import SessionLocal
from app.db import crud
import requests

PUBLISHER_URL = "http://localhost:9001"

router = APIRouter()
result = {}
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-ip")
async def get_ip():
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get("https://ipinfo.io/json")
            data = response.json()
            return {"ip": data["ip"]}
    except Exception as e:
        print(f"Error fetching IP address: {e}")
        return {"error": "Failed to fetch IP address"}
    
@router.post("/user_address")
async def get_address(event_data: dict = Body(...), db: Session = Depends(get_db)):
    user_id = event_data["user_id"]
    latitude = event_data["latitude"]
    longitude = event_data["longitude"]
    try:
        event_data = {
            "user_id": user_id,
            "longitud": longitude,
            "latitud": latitude}
        crud.create_user_location(db, event_data)
        return {"success": "User location created"}
    except Exception as e:
        print(f"Error creating user location: {e}")
        return {"error": "Failed to create user location"}