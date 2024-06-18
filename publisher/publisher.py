import paho.mqtt.client as mqtt
from fastapi import FastAPI,APIRouter, Depends, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import time
import json
import uvicorn

load_dotenv(".env", override=True) 


# Leer las credenciales desde el archivo .env
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
TOPIC_REQUEST = "flights/requests"
TOPIC_VALIDATION = "flights/validations"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
    else:
        print(f"Fallo en la conexión al broker MQTT, código de retorno: {rc}")

def on_publish(client,userdata,result):       
    print("data published \n")
    pass

# Mantener el cliente MQTT en funcionamiento

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:8001", "http://localhost:8002"],  # Replace with your frontend URL and port
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)



@app.post("/requests")
async def publish(event_data: dict = Body(...)):
    print("Publishing message")
    print(event_data)
    try:
        request = {
            "request_id": event_data["request_id"],
            "group_id": 23,
            "departure_airport": event_data["departure_airport_id"],
            "arrival_airport": event_data["arrival_airport_id"],
            "departure_time": event_data["time_departure"],
            "datetime": time.strftime('%Y-%m-%d %H:%M:%S'),
            "deposit_token": event_data["token"],
            "quantity": event_data["amount"],
            "seller": event_data["seller"],
        }
        print(request)
        request = json.dumps(request)
        client.publish(TOPIC_REQUEST, request)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/validations")
async def publish(event_data: dict = Body(...)):
    print("Publishing message validation")
    print(event_data)
    try:
        request = {
            "request_id": event_data["request_id"],
            "group_id": 23,
            "seller": event_data["seller"],
            "valid": event_data["valid"]
        }
        print(request)
        request = json.dumps(request)
        client.publish(TOPIC_VALIDATION, request)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":

    client = mqtt.Client("Publisher")
    client.username_pw_set(username=USER, password=PASSWORD)
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(HOST, PORT)
    uvicorn.run(app, host="0.0.0.0", port=9001)