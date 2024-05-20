import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, update  # Importar func desde SQLAlchemy
from .models import Airport, Flight, Ticket, Users, Prediction, UserLocation
from datetime import datetime, date, timedelta


#Función que recibe la información del evento y crea los vuelos y los aeropuertos
def create_event_with_flight(db: Session, event_data: dict):
    try:
        #Obtenermos la información que viene en el JSON del evento
        departure_airport_data = event_data["departure_airport"]
        departure_airport_id = departure_airport_data["id"]
        departure_airport_name = departure_airport_data["name"]
        arrival_airport_data = event_data["arrival_airport"]
        arrival_airport_id = arrival_airport_data["id"]
        arrival_airport_name = arrival_airport_data["name"]

        # Crear el objeto Airport para el aeropuerto de salida si no existe
        departure_airport = db.query(Airport).filter_by(id=departure_airport_id).first()
        if not departure_airport:
            departure_airport = Airport(id=departure_airport_id, name=departure_airport_name)
            print("Departure airport creado correctamente")
            db.add(departure_airport)

        # Crear el objeto Airport para el aeropuerto de llegada si no existe
        arrival_airport = db.query(Airport).filter_by(id=arrival_airport_id).first()
        if not arrival_airport:
            arrival_airport = Airport(id=arrival_airport_id, name=arrival_airport_name)
            print("Arrival airport creado correctamente")
            db.add(arrival_airport)

        #Creamos el objeto Flight con la información del vuelo y sus atributos
        flight = Flight(
            departure_airport_id=departure_airport.id,
            departure_airport_name=departure_airport.name,
            time_departure=departure_airport_data["time"],
            arrival_airport_id=arrival_airport.id,
            arrival_airport_name=arrival_airport.name,
            time_arrival=arrival_airport_data["time"],
            duration=event_data["duration"],
            airplane=event_data["airplane"],
            airline=event_data["airline"],
            airline_logo=event_data["airline_logo"],
            carbon_emissions=event_data["carbon_emissions"],
            price=event_data["price"],
            currency=event_data["currency"],
            seats_available= 90
        )
        
        # Agregar el vuelo a la sesión y confirmar la transacción
        db.add(flight)
        db.commit()
        db.refresh(flight)

        return flight

    except Exception as e:
        print("Error: ", e)
        db.rollback()
        raise

#RF1 - Función que obtiene los vuelos de la base de datos
def get_flights(
    db: Session, 
    departure: str = None,
    arrival: str = None, 
    date: str = None,
    skip: int = 0, 
    limit: int = 25
):
    #Obtenemos la fecha actual para filtrar vuelos pasados
    current_date = datetime.now()

    #Aplicar la consulta base para los vuelos
    query = db.query(Flight)

    #Aplicamos filtros si corresponde

    # Si se recibe alguno de los parámetros de búsqueda debemos solo mostrar los que no han salido!
    if (departure or arrival or date):
        # Filtrar vuelos cuya fecha de salida sea mayor o igual a la fecha actual
        query = query.filter(func.date(Flight.time_departure) >= current_date.date())  
        
    
    if departure: 
        query = query.filter(Flight.departure_airport_id == departure)
    if arrival: 
        query = query.filter(Flight.arrival_airport_id == arrival)
    if date:
        # Convertir la fecha de string a objeto date
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        # Filtrar vuelos cuya fecha de salida sea igual a la fecha indicada
        query = query.filter(func.date(Flight.time_departure) == date_obj)
    
    flights = query.offset(skip).limit(limit).all()  

    return flights
       
    
#RF2 - ofrecer un endpoint para mostrar el detalle de cada vuelo recibido desde el broker.
def get_flights_by_id(db: Session, flight_id: int, skip: int = 0, limit: int = 25):
    return (
        db.query(Flight)
        .filter(Flight.id == flight_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_ticket(db: Session, event_data: dict, ticket_id: uuid.UUID):
    try:
        #Obtenermos la información que viene en el JSON del evento
        departure_airport_id = event_data["departure_airport_id"]
        arrival_airport_id = event_data["arrival_airport_id"]
        user_id = event_data["user_id"]
        flight_id = int(event_data["flight_id"])
        time_departure = event_data["time_departure"]
        seller = event_data["seller"]
        status = event_data["status"]
        amount = int(event_data["amount"])

        #Creamos el objeto Ticket con la información del ticket y sus atributos
        ticket = Ticket(
            id=ticket_id,
            id_user=user_id,
            flight_id=flight_id,
            departure_airport_id=departure_airport_id,
            arrival_airport_id=arrival_airport_id,
            time_departure=time_departure,
            datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            seller=seller,
            status="pending",
            amount=amount
        )

        flight = db.query(Flight).filter(Flight.id == flight_id).first()
        new_seats_available = flight.seats_available - amount
        update_stmt = update(Flight).where(Flight.id == flight_id).values(seats_available=new_seats_available)
        db.execute(update_stmt)
        # Agregar el ticket a la sesión y confirmar la transacción
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return ticket
    except Exception as e:
        print("Error: ", e)
        db.rollback()
        raise

def update_ticket(db: Session, ticket_id: uuid.UUID, status: str):
    db.query(Ticket).filter(Ticket.id == ticket_id).update({Ticket.status: status})
    db.commit()

def get_tickets_by_id(db: Session, ticket_id: uuid.UUID):
    return (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
    )

def get_tickets_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 25):
    return (
        db.query(Ticket)
        .order_by(Ticket.time_departure.desc())
        .filter(Ticket.id_user == user_id)
        .all()
    )

def delete_ticket(db: Session, ticket_id: uuid.UUID):
    db.query(Ticket).filter(Ticket.id == ticket_id).delete()
    db.commit()

# # Creamos usuarios
# def create_user(db: Session, user: Users):
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# # Obtener usuarios
# def get_user_by_id(db: Session, user_id: int):
#     return db.query(Users).filter(Users.id == user_id).first()

# # Obtener usuario por email
# def get_user_by_email(db: Session, email: str):
#     return db.query(Users).filter(Users.email == email).first()

# # Obtener todos los usuarios
# def get_users(db: Session, skip: int = 0, limit: int = 25):
#     return db.query(Users).offset(skip).limit(limit).all()

def create_user_location(db: Session, event_data: dict):
    try:
        userLocation = UserLocation(
            id_user= event_data["user_id"],
            longitud= event_data["longitud"],
            latitude= event_data["latitud"]
        )
        db.add(userLocation)
        db.commit()
        db.refresh(userLocation)

        return userLocation
    except Exception as e:
        print("Error: ", e)
        db.rollback()
        raise

def update_user_location(db: Session, user_id: int, longitud: str, latitude: str):
    db.query(UserLocation).filter(UserLocation.id_user == user_id).update({UserLocation.longitud: longitud})
    db.query(UserLocation).filter(UserLocation.id_user == user_id).update({UserLocation.latitude: latitude})
    db.commit() 

def get_user_location(db: Session, user_id: int):
    return db.query(UserLocation).filter(UserLocation.id_user == user_id).all()

def create_prediction(db: Session, user_id: str, job_id:str,  recommended_flights: list):
    created_prediction = Prediction(
        id_user=user_id,
        job_id=job_id,
        datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        recommended_flights=recommended_flights,
        status="Pending"
    )
    db.add(created_prediction)
    db.commit()
    db.refresh(created_prediction)



def update_prediction(job_id: str, recommended_flights:list, db: Session):
    prediction = db.query(Prediction).filter(Prediction.job_id == job_id).first()
    prediction.recommended_flights = recommended_flights
    prediction.status = "Completed"
    db.commit()
    db.refresh(prediction)


def get_prediction(job_id: str, db: Session):
    query = (
        db.query(Prediction)
        .filter(Prediction.job_id == job_id)
        .first())
    return {'future_prices': query[1], 'future_dates': query[2], 'symbol': query[3], 'initial_date': query[4]}

def get_prediction_by_user(user_id: str, db: Session):
    return db.query(Prediction).filter(Prediction.id_user == user_id).all()

#Obtener el último ticker comprado por el usuario
def get_last_approved_ticket(db: Session, user_id: int):
    return db.query(Ticket).filter(
        Ticket.user_id == user_id,
        Ticket.status == "validated"
    ).order_by(Ticket.datetime.desc()).first()

# Obtener los ultimos 20 vuelos, respecto a la fecha de salida, que salgan dentro de la semana
# después de la compra, que vayan desde el aeropuerto de destino encontrado en el punto 2. 
def get_upcoming_flights(db: Session, airport_id: str, departure_date: datetime):
    week_after_purchase = departure_date + timedelta(days=7)
    return db.query(Flight).filter(
        Flight.departure_airport_id == airport_id,
        Flight.departure_time > departure_date,
        Flight.departure_time <= week_after_purchase
    ).order_by(Flight.departure_time.asc()).limit(20).all()


import requests

# Función para obtener las coordenadas del aeropuerto utilizando geocode.maps.co
def get_airport_coordinates(airport_id: str):
    try:
        # propia clave de API
        api_key = '6644d887417d1499696616bsid5ffd4'
        
        # URL de la API de geocodificación
        url = f'https://geocode.maps.co/v1/geocode?q={airport_id}&apikey={api_key}'

        # Realizar la solicitud GET a la API
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            # Extraer las coordenadas del resultado de la geocodificación
            location = data['results'][0]['geometry']['location']
            coordinates = (location['lat'], location['lng'])
            return coordinates
        else:
            return None
    except Exception as e:
        print(f"Error al obtener las coordenadas del aeropuerto: {str(e)}")
        return None

