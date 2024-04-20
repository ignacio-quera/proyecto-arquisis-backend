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


 # Creamos el modelo de usuario   

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    email: str
    password: str


 # Creamos el modelo de usuario   

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    email: str
    password: str

class Ticket(Base):

    __tablename__ = 'tickets'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer)
    departure_airport_id = Column(String)
    arrival_airport_id = Column(String)
    time_departure = Column(String)
    datetime = Column(DateTime)
    seller = Column(String)
    amount = Column(Integer)
    status = Column(String)

class TicketCreate(BaseModel):
    id: uuid.UUID
    user_id: int
    departure_airport_id: str
    arrival_airport_id: str
    time_departure: str
    datetime: str
    seller: str
    amount: int
    status: str