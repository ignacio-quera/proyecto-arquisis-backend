from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from app.db.database import SessionLocal
from app.db import crud

PUBLISHER_URL = "http://localhost:9001"

router = APIRouter()
result = {};
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
    
@router.get("/get-address")
async def get_address(ip: str, db: Session = Depends(get_db)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://ipinfo.io/{ip}/json")
            
            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()
                event_data = {
                    "user_id": "test",
                    "longitud":"",
                    "latitud": ""}
                
                crud.create_user_location(db, event_data)
                return {
                    "city": data["city"],
                    "region": data["region"],
                    "country": data["country"],
                    "loc": data["loc"],
                    "postal": data["postal"],
                    "timezone": data["timezone"],
                }
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    except Exception as e:
        print(f"Error fetching address: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch address")