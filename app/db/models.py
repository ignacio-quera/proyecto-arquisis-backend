from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from .database import Base
import uuid

class Airport(Base):
    __tablename__ = 'airports'

    id = Column(String, primary_key=True)
    name = Column(String)

class AirportCreate(BaseModel):
    name: str


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    departure_airport_id = Column(String, ForeignKey('airports.id'))
    departure_airport_name = Column(String)
    time_departure = Column(String)
    arrival_airport_id = Column(String, ForeignKey('airports.id'))
    arrival_airport_name = Column(String)
    time_arrival = Column(String)
    duration = Column(Integer)
    airplane = Column(String)
    airline = Column(String)
    airline_logo = Column(String)
    carbon_emissions = Column(Integer, nullable=True)  # Campo para emisiones de carbono
    price = Column(Integer)  # Campo para el precio del vuelo
    currency = Column(String)  # Campo para la moneda del precio
    seats_available = Column(Integer, default=90)  # Campo para los asientos disponibles
    

    departure_airport = relationship('Airport', foreign_keys=[departure_airport_id])
    arrival_airport = relationship('Airport', foreign_keys=[arrival_airport_id])

class FlightCreate(BaseModel):
    departure_airport_id: str
    departure_airport_name: str
    time_departure: str
    arrival_airport_id: str
    arrival_airport_name: str
    time_arrival: str
    duration: int
    airplane: str
    airline: str
    airline_logo: str
    carbon_emissions: int
    price: int
    currency: str
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    seats_available: int
=======
>>>>>>> aad0033 (subiendo cambios en users)
=======
    seats_available: int
>>>>>>> 61e2def (deploy ready)


 # Creamos el modelo de usuario   

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    email: str
    password: str
<<<<<<< HEAD

<<<<<<< HEAD
class Ticket(Base):

    __tablename__ = 'tickets'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flight_id = Column(Integer)
    id_user  = Column(String)
    departure_airport_id = Column(String)
    arrival_airport_id = Column(String)
    time_departure = Column(String)
    datetime = Column(String)
    seller = Column(String)
    amount = Column(Integer)
    status = Column(String)
        
class TicketCreate(BaseModel):
    id: uuid.UUID
    flight_id: int
    id_user: str
=======

=======
>>>>>>> c6d8a11 (User model fix)
class Ticket(Base):

    __tablename__ = 'tickets'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flight_id = Column(Integer)
    id_user  = Column(String)
    departure_airport_id = Column(String)
    arrival_airport_id = Column(String)
    time_departure = Column(String)
    datetime = Column(String)
    seller = Column(String)
    amount = Column(Integer)
    status = Column(String)
        
class TicketCreate(BaseModel):
    id: uuid.UUID
<<<<<<< HEAD
    user_id: int
>>>>>>> a4f89e8 (Adde listener and publisher, started ticket model)
=======
    flight_id: int
    id_user: str
>>>>>>> 61e2def (deploy ready)
    departure_airport_id: str
    arrival_airport_id: str
    time_departure: str
    datetime: str
    seller: str
    amount: int
<<<<<<< HEAD
<<<<<<< HEAD
    status: str
=======
    stauts: str
>>>>>>> a4f89e8 (Adde listener and publisher, started ticket model)
=======
    status: str
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
=======
>>>>>>> aad0033 (subiendo cambios en users)
