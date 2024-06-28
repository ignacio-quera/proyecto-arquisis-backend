from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from app.db import crud
from app.db.database import SessionLocal

router = APIRouter()
result = {};
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_flights(event_data: dict = Body(...), db: Session = Depends(get_db)):
    print("creando un vuelo")
    print(event_data)
    try:
        crud.create_airport(db, event_data) 
        crud.create_event_with_flight(db, event_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
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

ADMIN_ID = "auth0|666cd0831d14e274fd4dcc0d"


@router.get("/admin")
def read_flights_admin(
    page: int = Query(1, description="Page number", gt=0),
    count: int = Query(25, description="Number of items per page", gt=0, le=100),
    db: Session = Depends(get_db)
):
    # Calcular el offset
    skip = (page - 1) * count
    tickets = crud.get_admin_tickets(db, ADMIN_ID)
    print(tickets)
    if not tickets:
        return f"No hay ningún ticket"
    flights = []
    for ticket in tickets:
        flight = crud.get_flights_by_id(db, ticket.flight_id)
        flights.append(flight)
    if not flights:
        return "No hay información de vuelos disponible"

    return flights

# # Endpoint para mostrar el detalle de un vuelo por su identificador
@router.get("/{flight_id}")
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