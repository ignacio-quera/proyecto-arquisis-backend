from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from app.db import crud
from app.db.database import SessionLocal
from app.db.models import Flight
from app.db.models import Ticket
from typing import List
import uuid


router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_flights/")
def create_flights(event_data: dict = Body(...), db: Session = Depends(get_db)):
    print("creando un vuelo")
    print(event_data)
    try:
        crud.create_event_with_flight(db, event_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/flights/")
def read_flights(
    departure: str = Query(None, description="Departure airport code"),
    arrival: str = Query(None, description="Arrival airport code"),
    date: str = Query(None, description="Date of the flight"),
    page: int = Query(1, description="Page number", gt=0),
    count: int = Query(25, description="Number of items per page", gt=0, le=100),
    db: Session = Depends(get_db)
):
    # Calcular el offset
    skip = (page - 1) * count

    # Obtener los vuelos paginados desde la base de datos
    flights = crud.get_flights(db, departure=departure, arrival=arrival, date=date, skip=skip, limit=count)

    if not flights:
        return "No hay información de vuelos disponible"

    return flights


# # Endpoint para mostrar el detalle de un vuelo por su identificador
@router.get("/flights/{flight_id}")
def read_flight_by_id(
    flight_id: int,
    page: int = Query(1, description="Page number", gt=0),
    size: int = Query(25, description="Number of items per page", gt=0, le=150),
    db: Session = Depends(get_db)
    ):

    skip = (page - 1) * size
    flights = crud.get_flights_by_id(db, flight_id, skip=skip, limit=size)

    if not flights:
        return f"No hay ningún vuelo con id {flight_id}"
    
    return flights

# # Endpoint para mostrar el detalle de un vuelo por su identificador
@router.get("/airports/")
def read_aiports(
    page: int = Query(1, description="Page number", gt=0),
    size: int = Query(25, description="Number of items per page", gt=0, le=150),
    db: Session = Depends(get_db)
    ):

    skip = (page - 1) * size
    airports = crud.get_airports(db, skip=skip, limit=size)

    if not airports:
        return f"No hay ningún aeropuerto"
    
    return airports

@router.post("/create_ticket/")
def create_ticket(ticket: Ticket, db: Session = Depends(get_db)):
    print("creando un ticket")
    ticket.id = uuid.uuid4() 
    ticket_request = {
        "id": str(ticket.id),
        "user_id": ticket.user_id,
        "departure_airport_id": ticket.departure_airport_id,
        "arrival_airport_id": ticket.arrival_airport_id,
        "time_departure": ticket.time_departure,
        "datetime": ticket.datetime,
        "seller": ticket.seller,
        "amount": ticket.amount,
        "status": ticket.status
    }
    try:
        crud.create_ticket(db, ticket_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/update_ticket/")
def update_ticket(ticket: Ticket, db: Session = Depends(get_db)):
    print("actualizando un ticket")
    ticket_request = {
        "id": str(ticket.id),
        "user_id": ticket.user_id,
        "departure_airport_id": ticket.departure_airport_id,
        "arrival_airport_id": ticket.arrival_airport_id,
        "time_departure": ticket.time_departure,
        "datetime": ticket.datetime,
        "seller": ticket.seller,
        "amount": ticket.amount,
        "status": ticket.status
    }
    try:
        crud.update_ticket(db, ticket_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))