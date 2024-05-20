from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
import requests
import uuid
from app.db import crud
from app.db.database import SessionLocal
from celery_config.tasks import flight_prediction

router = APIRouter()
result = {}
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/make_prediction")
async def make_prediction(request: Request, db: Session = Depends(get_db)):
    user_id = request.headers.get("user")
    try:
        if not user_id:
            raise ValueError("User ID is required in the headers")

        # Example logic to fetch last purchase and extract airport name
        last_purchase = crud.get_last_approved_ticket(db, user_id)  
        if not last_purchase:
            raise HTTPException(status_code=404, detail="No purchase found")

        airport_name = last_purchase['arrival_airport_id']
        departure_date = last_purchase['time_departure']
        
        upcoming_flights = crud.get_upcoming_flights(db, airport_name, departure_date)  
        user_location = crud.get_user_location(db, user_id)
        
        flight_details = []
        for flight in upcoming_flights:
            flight_coords = crud.get_airport_coordinates(flight['arrival_airport_id'])
            flight_details.append({'flight': flight, 'coordinates': flight_coords})

        result = flight_prediction.delay(flight_details, user_location)

        # Return a response with the Celery task ID
        return {"message": "Recommendation calculation in progress", "task_id": result.id}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/prediction")
async def get_prediction(request: Request, db: Session = Depends(get_db)):
    user_id = request.headers.get("user")
    try:
        if not user_id:
            raise ValueError("User ID is required in the headers")

        prediction = crud.get_prediction(db, user_id)
        if not prediction:
            raise HTTPException(status_code=404, detail="No prediction found")

        return prediction

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))