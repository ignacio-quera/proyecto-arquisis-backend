from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks
from sqlalchemy.orm import Session
import requests
import httpx
from app.db import crud
from app.db.database import SessionLocal
<<<<<<< HEAD
from app.db.models import  Users, UserCreate
=======
from app.db.models import Flight
from app.db.models import Ticket
from typing import List
import uuid
>>>>>>> a4f89e8 (Adde listener and publisher, started ticket model)


PUBLISHER_URL = "http://localhost:9001"

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

<<<<<<< HEAD

@router.post("/new_ticket/")
async def create_ticket(background_tasks: BackgroundTasks, event_data: dict = Body(...), db: Session = Depends(get_db)):
    print("creando un ticket")
    print(event_data)
    try:
        crud.create_ticket(db, event_data)
        # response = requests.post(f"{PUBLISHER_URL}/requests/", json={"topic": "flights/validation", "message": event_data})
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{PUBLISHER_URL}/requests", json={"topic": "flights/validation", "message": event_data})
                data = response.json()
        except Exception as e:
            print(f"Error validating ticket: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/update_ticket/")
def update_ticket(event_data: dict = Body(...), db: Session = Depends(get_db)):
    print("actualizando un ticket")
    try:
        ticket_id = event_data["ticket_id"]
        crud.update_ticket(db, ticket_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/tickets/{user_id}")
def read_tickets(
    user_id: str,
    db: Session = Depends(get_db)
    ):

    tickets = crud.get_tickets_by_id(db, user_id)

    if not tickets:
        return f"No hay ningún ticket"
    
    return tickets


# # Endpoint para crear un usuario, que devuelva al usuario creado
@router.post("users/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print("Registrando un usuario")
    print(user)
    # Verificar si el usuario ya existe en la base de datos
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear un nuevo usuario utilizando los datos proporcionados
    new_user = Users(email=user.email, hashed_password= user.password)

    # Llamar a la función de CRUD para crear el usuario en la base de datos
    created_user = crud.create_user(db=db, user=new_user)

    return {"message": "User created successfully"}


# # Endpoint para obtener un usuario por su identificador
@router.get("/users/{user_id}")
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# # Endpoint para obtener todos los usuarios
@router.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

# # Endpoint para obtener un usuario por su email
@router.get("/users/email/{email}")
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/get-ip")
async def get_ip():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://ipinfo.io/json")
            data = response.json()
            return {"ip": data["ip"]}
    except Exception as e:
        print(f"Error fetching IP address: {e}")
        return {"error": "Failed to fetch IP address"}
    
@router.get("/get-address")
async def get_address(ip: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://ipinfo.io/{ip}/json")
            
            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()
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


=======
@router.post("/create_ticket/")
def create_ticket(
    event_data: dict = Body(...),
    db: Session = Depends(get_db)
    ):
    print("creando un ticket")
<<<<<<< HEAD
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
<<<<<<< HEAD
    return crud.create_ticket(db, ticket)
>>>>>>> a4f89e8 (Adde listener and publisher, started ticket model)
=======
=======
    print(event_data)
>>>>>>> e7a2b5d (Cambios tickets)
    try:
        crud.create_ticket(db, event_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
<<<<<<< HEAD
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
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
=======
# @router.patch("/update_ticket/")
# def update_ticket(ticket: Ticket, db: Session = Depends(get_db)):
#     print("actualizando un ticket")
#     ticket_request = {
#         "id": str(ticket.id),
#         "user_id": ticket.user_id,
#         "departure_airport_id": ticket.departure_airport_id,
#         "arrival_airport_id": ticket.arrival_airport_id,
#         "time_departure": ticket.time_departure,
#         "datetime": ticket.datetime,
#         "seller": ticket.seller,
#         "amount": ticket.amount,
#         "status": ticket.status
#     }
#     try:
#         crud.update_ticket(db, ticket_request)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/tickets/")
def read_tickets(
    page: int = Query(1, description="Page number", gt=0),
    size: int = Query(25, description="Number of items per page", gt=0, le=150),
    db: Session = Depends(get_db)
    ):

    skip = (page - 1) * size
    tickets = crud.get_tickets(db, skip=skip, limit=size)

    if not tickets:
        return f"No hay ningún ticket"
    
    return tickets
>>>>>>> e7a2b5d (Cambios tickets)
