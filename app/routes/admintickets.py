from fastapi import APIRouter, Depends, HTTPException, Body, Request, status
from sqlalchemy.orm import Session
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
from transbank.error.transbank_error import TransbankError
from fastapi.security import OAuth2PasswordBearer
import requests
import random
import uuid
import json
from app.db import crud
from app.db.database import SessionLocal
from dotenv import load_dotenv
import os
import httpx 

def get_current_user_role(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    # Decode token

    if token == "admin_token":
        return "admin"
    else:
        return "user"

# Dependency to check if the user is an admin
def admin_required(role: str = Depends(get_current_user_role)):
    #return;
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the necessary permissions to access this resource."
        )

def get_airport_coordinates(airport_code):
    base_url = "https://geocode.maps.co"
    params = {'q': airport_code}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        # Filter results to find an entry that matches an airport type
        airport_result = next((item for item in results if item['type'] == 'aerodrome'), None)
        if airport_result:
            lat = airport_result['lat']
            lon = airport_result['lon']
            return (lat, lon)
        else:
            return None  # No airport found in the filtered results
    else:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")


# Especifica la ruta completa al archivo .env que deseas cargar
load_dotenv(".env") 

#PUBLISHER_URL = "http://publisher_container:9001"
FRONTEND_URL = "http://localhost:3000"
ADMIN_ID = os.getenv("ADMIN_USER_ID")
ADMIN_ID = "google-oauth2|106408141437006333297"
# FRONTEND_URL = "https://www.angegazituae0.me"

router = APIRouter()
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def get_admin_tickets(
    request: Request,
    db: Session = Depends(get_db)
    ):
    seller = "23"
    tickets = crud.get_admin_tickets(db, ADMIN_ID)
    print(tickets)
    if not tickets:
        return f"No hay ningún ticket"
    return tickets

@router.post("/", dependencies=[Depends(admin_required)])
async def update_ticket_for_user(event_data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        request_id = uuid.uuid4()
        ticket = crud.update_ticket_user(db, event_data)
        event_data["request_id"] = str(request_id)
        # ticket_id = str(event_data["ticket_id"])
        # flight_id = str(event_data["flight_id"])
        # amount = str(event_data["amount"])
        return_url = f"{FRONTEND_URL}/compracompletada?ticket_id={ticket.id}&flight_id={ticket.flight_id}&amount={ticket.amount}"
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        buy_order = str(random.randrange(1000000, 99999999))
        try:
            result = tx.create(buy_order, event_data["request_id"], event_data["amount"], return_url)
            event_data["token"] = result["token"]
            #ticket = crud.update_ticket_user(db, event_data, request_id)
            #requests.post(f'{PUBLISHER_URL}/requests', json=event_data)
            return result
        except TransbankError as e:
            print(e.message)
            return {"error": e.message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/")
def update_ticket(event_data: dict = Body(...), db: Session = Depends(get_db)):
    print("actualizando un ticket")
    try:
        ticket_id = event_data["request_id"]
        status = event_data["valid"]
        crud.update_ticket(db, ticket_id, status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
def delete_ticket(
    request: Request,
    db: Session = Depends(get_db)):
    print("borrando un ticket")
    try:
        ticket_id = request.headers["ticket_id"]
        print(ticket_id, type(ticket_id))
        id_user = request.headers["user"]
        crud.delete_ticket(db, ticket_id)
        tickets = crud.get_tickets_by_user_id(db, id_user)
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ticket_id}")
def get_tickets_by_id(
    ticket_id: str,
    db: Session = Depends(get_db)
    ):
    print(ticket_id, type(ticket_id))
    ticket_uid = uuid.UUID(ticket_id)
    print(ticket_uid, type(ticket_uid))
    ticket = crud.get_tickets_by_id(db, ticket_uid)
    if not ticket:
        return f"No hay ningún ticket con id {ticket_id}"
    return ticket

@router.post("/{ticket_id}/discount", dependencies=[Depends(admin_required)])
def apply_discount(
    ticket_id: str,
    request: Request,
    db: Session = Depends(get_db)
    ):
    discount_percentage = int(request.headers["discount"])
    print(discount_percentage, type(discount_percentage))
    print(ticket_id, type(ticket_id))
    ticket_uid = uuid.UUID(ticket_id)
    print(ticket_uid, type(ticket_uid))
    ticket = crud.apply_discount_to_ticket(db, ticket_uid, discount_percentage)
    return ticket
