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
        print(event_data)
        auction_id = uuid.uuid4()
        print(auction_id)
        event_data["auction_id"] = auction_id
        print(event_data)
        requests.post(f'{PUBLISHER_URL}/auctions', json=event_data)
        return {'message': 'Auction created successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))