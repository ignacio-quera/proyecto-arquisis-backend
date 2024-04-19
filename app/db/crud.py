from sqlalchemy.orm import Session
from sqlalchemy import func  # Importar func desde SQLAlchemy
from .models import Airport, Flight, Ticket
from datetime import datetime, date
from sqlalchemy.orm import aliased

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
            currency=event_data["currency"]
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

def create_ticket(db: Session, ticket: Ticket):
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def update_ticket(db: Session, ticket: Ticket):
    db.query(Ticket).filter(Ticket.uuid == ticket.uuid).update({Ticket.status: ticket.status})
    db.commit()
    return ticket