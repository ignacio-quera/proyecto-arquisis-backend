from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
import requests
import uuid
from app.db import crud
from app.db.database import SessionLocal
import httpx
import traceback
import logging

PRODUCER_URL = "http://producer_container:8005"

router = APIRouter()
result = {}
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def make_prediction(request: Request, db: Session = Depends(get_db)):
    print("adentro de make_prediction")
    try:
        data = await request.json()
        user_id = data["user_id"]
        # # Example logic to fetch last purchase and extract airport name
        last_purchase = crud.get_last_approved_ticket(db, user_id) 

        airport_name = last_purchase.arrival_airport_id
        departure_date = last_purchase.time_departure
        upcoming_flights = crud.get_upcoming_flights(db, airport_name, departure_date)  
        
        user_location = crud.get_user_location(db, user_id)
        flight_details = []
        for flight in upcoming_flights:
            flight_coords = crud.get_airport_coordinates(db, flight.arrival_airport_id)
            flight_details.append({
                'flight_id': flight.id,
                'departure_airport_id': flight.departure_airport_id,
                'arrival_airport_id': flight.arrival_airport_id,
                'time_departure': flight.time_departure,
                'time_arrival': flight.time_arrival,
                'price': flight.price,
                'coordinates': flight_coords
            })

        data = {
            "flight_details": flight_details,
            "user_location": {
                'latitude': user_location.latitude,
                'longitude': user_location.longitud
            }
        }

        # #result = flight_prediction.delay(flight_details, user_location)
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{PRODUCER_URL}/job", json=data)

        print("WE GOT AN ANSWER")
        print(response)
        # Return a response with the Celery task ID
        if response.status_code == 200:
            data = response.json()
            print(data)
            job_id = data["job_id"]
            print(job_id)
            #(db: Session, user_id: str, job_id:str,  recommended_flights: list
            crud.create_prediction(db, user_id, job_id)
            return {"message": "Operación exitosa"}
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al realizar la solicitud externa")
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Obtener la traza completa del error
        error_trace = traceback.format_exc()
        
        # Crear un mensaje detallado
        detailed_error_message = f"Error: {str(e)}\nTraceback: {error_trace}"
        
        # Lanzar una excepción HTTP con el mensaje detallado
        raise HTTPException(status_code=500, detail=detailed_error_message) 
    
# @router.get("/prediction/")
# async def get_prediction(request: Request, db: Session = Depends(get_db)):
#     user_id = request.headers.get("user")
#     try:
#         if not user_id:
#             raise ValueError("User ID is required in the headers")
#         print("hola")
#         prediction = crud.get_prediction_by_user(db, user_id)
#         print(prediction)
#         if not prediction:
#             raise HTTPException(status_code=404, detail="No prediction found")

#         return prediction

#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_user_predictions(request: Request, db: Session = Depends(get_db)):
    user_id = request.headers.get("user")
    print(request.headers)
    print(user_id)
    predictions = crud.get_prediction_by_user(user_id, db)
    
    for prediction in predictions:
        print(prediction)
        if prediction.status == "Pending":
            job_id = prediction.job_id
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{PRODUCER_URL}/job/{job_id}")
                
                data = response.json()
                if data is not None:
                    print(data)
                    recommended_flights = data["result"]
                    crud.update_prediction(job_id, recommended_flights, db)
            
            except Exception as e:
                logging.error(f"Error: {e}")
                raise HTTPException(status_code=500, detail="Se produjo un error interno en el servidor")
    
    return crud.get_prediction_by_user(user_id, db)