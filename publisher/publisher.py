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
TOPIC = "flights/requests"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
    else:
        print(f"Fallo en la conexión al broker MQTT, código de retorno: {rc}")

def on_publish(client,userdata,result):       
    print("data published \n")
    pass


client = mqtt.Client("Publisher")
client.username_pw_set(username=USER, password=PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish

# Mantener el cliente MQTT en funcionamiento

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:8001", "http://localhost:8002"],  # Replace with your frontend URL and port
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


router = APIRouter()

@router.post("/requests")
async def publish(event_data: dict = Body(...)):
    print("Publishing message")
    try:
        message = json.dumps(event_data)
        await client.publish(TOPIC, message)
        # print(event_data)
        return {"message": "Message published successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    client.connect(HOST, PORT)
    uvicorn.run(app, host="0.0.0.0", port=9001)