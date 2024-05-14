from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
import requests
import uuid
from app.db import crud
from app.db.database import SessionLocal
# from worker_tasks import flight_prediction 
import httpx

def get_airport_coordinates(airport_code):
    base_url = "https://geocode.maps.co"
    params = {'q': airport_code}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        # Filter results to find an entry that matches an airport type
        airport_result = next((item for item in results if item['type'] == 'aerodrome'), None)
        if airport_result:
            lat = airport_result['lat']
            lon = airport_result['lon']
            return (lat, lon)
        else:
            return None  # No airport found in the filtered results
    else:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")


def get_airport_coordinates(airport_name):
    base_url = "https://geocode.maps.co"
    params = {'q': airport_name}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        if results:
            first_result = results[0]  # Assuming the first result is the most relevant
            lat = first_result['lat']
            lon = first_result['lon']
            return (lat, lon)
        else:
            return None
    else:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")


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

@router.get("/")
async def read_tickets(
    request: Request,
    db: Session = Depends(get_db)
    ):
    headers = dict(request.headers)
    user_id = headers.get("user")
    tickets = crud.get_tickets_by_id(db, user_id)

    if not tickets:
        return f"No hay ningún ticket"
    
    return tickets

@router.post("/create/")
async def create_ticket(background_tasks: BackgroundTasks, event_data: dict = Body(...), db: Session = Depends(get_db)):
    print("creando un ticket")
    print(event_data)
    try:
        id = uuid.uuid4()
        crud.create_ticket(db, event_data, id)
        event_data["request_id"] = str(id)
        service_url = "http://publisher_container:9001/requests"
        response = requests.post(service_url, json=event_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/update/")
def update_ticket(event_data: dict = Body(...), db: Session = Depends(get_db)):
    print("actualizando un ticket")
    try:
        ticket_id = event_data["request_id"]
        crud.update_ticket(db, ticket_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))