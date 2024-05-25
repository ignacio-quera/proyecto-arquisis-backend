from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
import requests
import uuid
from app.db import crud
from app.db.database import SessionLocal
import httpx
import traceback

router = APIRouter()
result = {}
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/heartbeat")
async def heartbeat():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://producer:8000/heartbeat")
            return response.json()
    except Exception as e:
        return {"status": "down"}