import paho.mqtt.client as mqtt
import time
import multiprocessing
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv("env", override=True) 

# Leer las credenciales desde el archivo .env
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
TOPIC = "flights/requests"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
        client.subscribe("flights/info")
    else:
        print(f"Fallo en la conexión al broker MQTT, código de retorno: {rc}")

def on_publish(client,userdata,result):       
    print("data published \n")
    pass


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(username=USER, password=PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish

print("Conectando al broker MQTT...")
client.connect(HOST, PORT, keepalive=60)

# Mantener el cliente MQTT en funcionamiento
client.loop_forever()