from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
import requests
import httpx
import uuid
from app.db import crud
from app.db.database import SessionLocal
from app.db.models import  Users, UserCreate


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


@router.post("/new_ticket/")
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
    
@router.patch("/update_ticket/")
def update_ticket(event_data: dict = Body(...), db: Session = Depends(get_db)):
    print("actualizando un ticket")
    try:
        ticket_id = event_data["request_id"]
        crud.update_ticket(db, ticket_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/tickets/")
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


