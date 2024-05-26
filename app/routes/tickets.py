from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
# from botocore.exceptions import ClientError
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
from transbank.error.transbank_error import TransbankError
import requests
import random
import uuid
import json
from app.db import crud
from app.db.database import SessionLocal
import httpx


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


def get_airport_coordinates(airport_name):
    base_url = "https://geocode.maps.co"
    params = {'q': airport_name}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        if results:
            first_result = results[0]  # Assuming the first result is the most relevant
            lat = first_result['lat']
            lon = first_result['lon']
            return (lat, lon)
        else:
            return None
    else:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")


PUBLISHER_URL = "http://publisher_container:9001"
# FRONTEND_URL = "http://localhost:3000"
FRONTEND_URL = "https://www.angegazituae0.me"

router = APIRouter()
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def read_tickets(
    request: Request,
    db: Session = Depends(get_db)
    ):
    headers = dict(request.headers)
    user_id = headers.get("user")
    tickets = crud.get_tickets_by_user_id(db, user_id)

    if not tickets:
        return f"No hay ningún ticket"
    return tickets

@router.get("/{ticket_id}")
def get_ticket_by_id(
    ticket_id: int,
    db: Session = Depends(get_db)
    ):
    ticket = crud.get_ticket_by_id(db, ticket_id)
    if not ticket:
        return f"No hay ningún ticket con id {ticket_id}"
    return ticket

@router.post("/create/")
async def create_ticket(event_data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        request_id = uuid.uuid4()
        crud.create_ticket(db, event_data, request_id)
        event_data["request_id"] = str(request_id)
        return_url = f"{FRONTEND_URL}/compracompletada"
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        buy_order = str(random.randrange(1000000, 99999999))
        try:
            result = tx.create(buy_order, event_data["request_id"], event_data["amount"], return_url)
            event_data["token"] = result["token"]
            requests.post(f'{PUBLISHER_URL}/requests', json=event_data)
            return result
        except TransbankError as e:
            print(e.message)
            return {"error": e.message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/update/")
def update_ticket(event_data: dict = Body(...), db: Session = Depends(get_db)):
    print("actualizando un ticket")
    try:
        ticket_id = event_data["request_id"]
        status = event_data["valid"]
        crud.update_ticket(db, ticket_id, status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
def delete_ticket(
    request: Request,
    db: Session = Depends(get_db)):
    print("borrando un ticket")
    try:
        ticket_id = request.headers["ticket_id"]
        print(ticket_id, type(ticket_id))
        id_user = request.headers["id_user"]
        crud.delete_ticket(db, ticket_id)
        tickets = crud.get_tickets_by_user_id(db, id_user)
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
