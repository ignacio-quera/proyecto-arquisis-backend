# from fastapi import APIRouter, Depends, HTTPException, Query, Body
# from .publisher import client

# router = APIRouter()

# @router.post("/requests")
# async def publish(topic: str = Query(..., min_length=1), message: str = Body(..., min_length=1)):
#     try:
#         print("TEST")
#         await client.publish(topic, message)
#         return {"message": "Message published successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
