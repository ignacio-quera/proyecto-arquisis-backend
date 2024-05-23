from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
import requests
import uuid
from app.db import crud
from app.db.database import SessionLocal
import httpx
import traceback

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
    #user_id = request.headers.get("user")
    print("adentro de make_prediction")
    try:
        data = await request.json()
        user_id = data["user_id"]
        print(user_id)
        print(type(user_id))
        print("entramos al try")
        # if not user_id:
        #    raise ValueError("User ID is required in the headers")

        # # Example logic to fetch last purchase and extract airport name
        last_purchase = crud.get_last_approved_ticket(db, user_id) 
        print(last_purchase) 
        # if not last_purchase:
        #     raise HTTPException(status_code=404, detail="No purchase found")

        airport_name = last_purchase.arrival_airport_id
        print(airport_name)
        departure_date = last_purchase.time_departure
        print(departure_date)
        print(type(departure_date))
        
        upcoming_flights = crud.get_upcoming_flights(db, airport_name, departure_date)  
        print(upcoming_flights)
        
        print("user location")
        user_location = crud.get_user_location(db, user_id)
        print(user_location)
        
        flight_details = []
        for flight in upcoming_flights:
            flight_coords = crud.get_airport_coordinates(flight.arrival_airport_id)
            flight_details.append({'flight': flight, 'coordinates': flight_coords})
        data = {"flight_details": flight_details, "user_location": user_location}
        print(data)

        # #result = flight_prediction.delay(flight_details, user_location)
        async with httpx.AsyncClient(timeout=30.0) as client:
            print("llamamos a post")
            url = "http://producer:8000/job"
            #response = await client.get("http://producer:8000/job")
            response = await client.post("http://producer:8000/job", json=data)

        print("WE GOT AN ANSWER")
        print(response)
        # # Return a response with the Celery task ID
        return {"message": "Recommendation calculation in progress", "task_id": result.id}
        # if response.status_code == 200:
        #     data = response.json()
        #     print(data)
        #     job_id = data["job_id"]
        #     #(db: Session, user_id: str, job_id:str,  recommended_flights: list
        #     crud.create_prediction(db, user_id, job_id, data)
        #     return {"message": "Operación exitosa"}
        # else:
        #     raise HTTPException(status_code=response.status_code, detail="Error al realizar la solicitud externa")
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Obtener la traza completa del error
        error_trace = traceback.format_exc()
        
        # Crear un mensaje detallado
        detailed_error_message = f"Error: {str(e)}\nTraceback: {error_trace}"
        
        # Lanzar una excepción HTTP con el mensaje detallado
        raise HTTPException(status_code=500, detail=detailed_error_message) 
    
@router.get("/prediction/")
async def get_prediction(request: Request, db: Session = Depends(get_db)):
    user_id = request.headers.get("user")
    try:
        if not user_id:
            raise ValueError("User ID is required in the headers")

        prediction = crud.get_prediction_by_user(db, user_id)
        if not prediction:
            raise HTTPException(status_code=404, detail="No prediction found")

        return prediction

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/predictions/")
async def list_user_predictions(user_id: str, db: Session = Depends(get_db)):
    predictions = crud.get_prediction_by_user(db, user_id)
    
    for prediction in predictions:
        if prediction["status"] == "Pending":
            job_id = prediction["job_id"]
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"http://producer:8000/job/{job_id}")
                
                data = response.json()
                if data is not None:
                    recommended_flights = data["result"]
                    crud.update_prediction(job_id, recommended_flights, db)
            
            except Exception as e:
                logging.error(f"Error: {e}")
                raise HTTPException(status_code=500, detail="Se produjo un error interno en el servidor")
    
    return crud.get_user_predictions(user_id, db)