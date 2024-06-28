from fastapi import APIRouter, Depends, HTTPException, Query, Body
from .mqtt_publisher import client

router = APIRouter()

@router.post("/publish")
async def publish(topic: str = Query(..., min_length=1), message: str = Body(..., min_length=1)):
    try:
        
        await client.publish(topic, message)
        return {"message": "Message published successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
