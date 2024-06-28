from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
import requests
import random
import uuid
import json
from app.db import crud
from app.db.database import SessionLocal
from dotenv import load_dotenv
import os
import httpx 

PUBLISHER_URL = "http://publisher_container:9001"

router = APIRouter()
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def create_auction_offer(event_data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        auction_id = uuid.uuid4()
        auction = crud.create_auction(db, event_data, auction_id)
        requests.post(f'{PUBLISHER_URL}/auctions', json=event_data)
        return {'message': 'Auction created successfully'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/proposal")
async def create_auction_proposal(event_data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        proposal_id = uuid.uuid4()
        event_data["proposal_id"] = str(proposal_id)
        requests.post(f'{PUBLISHER_URL}/auctions', json=event_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/")
async def update_auction_offer(event_data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        auction_id = event_data["auction_id"]
        auction = crud.update_auction(db, event_data)
        return auction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_auctions(
        db: Session = Depends(get_db)
    ):
    auctions = crud.get_auctions(db)
    if not auctions:
        return f"No hay ninguna subasta"
    return auctions

@router.get("/{auction_id}")
async def get_auction_by_id(
    auction_id: str,
    db: Session = Depends(get_db)
    ):
    auction = crud.get_auction_by_id(db, auction_id)
    if not auction:
        return f"No hay ninguna subasta con id {auction_id}"
    return auction
    