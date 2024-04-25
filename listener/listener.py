<<<<<<< HEAD
import paho.mqtt.client as mqtt
import time
import multiprocessing
import json
import requests
from dotenv import load_dotenv
import os
from topic_handler import handleFlightInfo, handleTicketValidation

# Especifica la ruta completa al archivo .env que deseas cargar
load_dotenv("mqtt_listener.env", override=True) 
<<<<<<< HEAD
=======
<<<<<<< HEAD
import requests
=======
import paho.mqtt.client as mqtt
import time
import multiprocessing
>>>>>>> a4f89e8 (Adde listener and publisher, started ticket model)
import json
import os
from topic_handler import handleFlightInfo, handleTicketValidation

<<<<<<<< HEAD:listener/topic_handler.py
========
# Especifica la ruta completa al archivo .env que deseas cargar
load_dotenv(".env", override=True) 
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
=======
>>>>>>> 78f69df (listener corriendo correctamente)

# Leer las credenciales desde el archivo .env
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
<<<<<<< HEAD
<<<<<<< HEAD
API_URL = os.getenv("API_URL")
=======
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
=======
API_URL = os.getenv("API_URL")
>>>>>>> 61e2def (deploy ready)

topicHandlers = {
  'flights/info': handleFlightInfo,
  'flights/validation': handleTicketValidation,
};

# Callback cuando se conecta al broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
        client.subscribe("flights/info")
        client.subscribe("flights/validation")
    else:
        print(f"Fallo en la conexión al broker MQTT, código de retorno: {rc}")


# Callback cuando llega un mensaje MQTT
def on_message(client, userdata, msg):
<<<<<<< HEAD

    try:
=======
<<<<<<< HEAD
    print(f"Mensaje recibido en el tópico {msg.topic}: {msg.payload}")

    api_url = "http://fastapi_app:8000/create_flights/"
    payload = msg.payload.decode()
    #Lo transformamos a un objeto de python
    data = json.loads(payload)
>>>>>>>> 952861c (publisher and listener init):listener/mqtt_listener.py
=======
>>>>>>> a4f89e8 (Adde listener and publisher, started ticket model)

def handleFlightInfo(data):
    try:
<<<<<<< HEAD
        flight_info = data[0]  # Primer elemento de la lista
        #Esto me da un string
        flights_json = flight_info.get("flights", "[]")
        flights = json.loads(flights_json)
        #Ver si esto me da un str o un diccionario
        flight = flights[0]

        #Tengo un diccionario de un vuelo, accedamos a sus elementos
        departure_airport = flight["departure_airport"]
        departure_airport_id = departure_airport["id"]
        departure_airport_name = departure_airport["name"]
        departure_time = departure_airport["time"]
        arrival_airport = flight["arrival_airport"]
        arrival_airport_id = arrival_airport["id"]
        arrival_airport_name = arrival_airport["name"]
        arrival_time = arrival_airport["time"]
        duration = int(flight["duration"])
        airplane = flight["airplane"]
        airline = flight["airline"]
        airline_logo = flight["airline_logo"]

        #Tenemos un string
        carbon_emissions = flight_info["carbonEmission"]
        #Lo transformamos a diccionario
        carbon_emissions = json.loads(carbon_emissions)
        carbon_emissions = carbon_emissions["this_flight"] 
        price = int(flight_info.get("price"))
        currency = flight_info.get("currency")
        airline_logo = flight_info.get("airlineLogo")

        #Creamos nuestro JSON con todos los datos que necesitamos
        flight_json = {
            "departure_airport": departure_airport,
            "arrival_airport": arrival_airport,
            "time_departure": departure_time,
            "duration": duration,
            "airplane": airplane,
            "airline": airline,
            "airline_logo": airline_logo,
            "carbon_emissions": carbon_emissions,
            "price": price,
            "currency": currency,
            "airline_logo": airline_logo
        }
        
        response = requests.post(os.getenv("API_URL")+"/create_flights/", json=flight_json) 
        if response.status_code == 200:
            print("Mensaje enviado a la API con éxito.")
        else:
            print("Error al enviar el mensaje a la API:", response.text)
    except json.JSONDecodeError as e:
        print("Error al decodificar el mensaje JSON:", e)
    except requests.exceptions.RequestException as e:
        print("Error al enviar el mensaje a la API:", e)

def handleTicketValidation(data):
=======
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
        print(f"Mensaje recibido en el tópico {msg.topic}: {msg.payload}")
        payload = msg.payload.decode()
        #Lo transformamos a un objeto de python
        data = json.loads(payload)
        topicHandlers[msg.topic](data)
    except KeyError as e:
        print(f"Error al manejar el mensaje: {e}")


<<<<<<< HEAD
<<<<<<< HEAD
# print("Starting MQTT listener")
# client = mqtt.Client()
=======
# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
=======
# print("Starting MQTT listener")
# client = mqtt.Client()
>>>>>>> 78f69df (listener corriendo correctamente)
# client.on_connect = on_connect
# client.on_message = on_message
# client.username_pw_set(username=USER, password=PASSWORD)

<<<<<<< HEAD
<<<<<<< HEAD
=======
# print("Conectando al broker MQTT...")
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
=======
>>>>>>> 78f69df (listener corriendo correctamente)
# client.connect(HOST, PORT)
# client.loop_forever()

# Función para iniciar el cliente MQTT
def start_mqtt_client():
<<<<<<< HEAD
<<<<<<< HEAD
    print("Conectando al broker MQTT...")
    client = mqtt.Client()
=======
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
=======
    print("Conectando al broker MQTT...")
    client = mqtt.Client()
>>>>>>> 78f69df (listener corriendo correctamente)
    client.username_pw_set(username=USER, password=PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    client.connect(HOST, PORT)
=======
    print("Conectando al broker MQTT...")
=======
>>>>>>> 78f69df (listener corriendo correctamente)
    client.connect(HOST, PORT, keepalive=60)
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
=======
    client.connect(HOST, PORT)
>>>>>>> 61e2def (deploy ready)
    
    # Mantener el cliente MQTT en funcionamiento
    client.loop_forever()

if __name__ == "__main__":
    # Crear un proceso independiente para el cliente MQTT
    mqtt_process = multiprocessing.Process(target=start_mqtt_client)
    mqtt_process.start()

<<<<<<< HEAD
    try:
        while True:
            # Mantener el proceso principal en funcionamiento
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo el proceso MQTT...")
        mqtt_process.terminate()
=======
>>>>>>> a4f89e8 (Adde listener and publisher, started ticket model)
    try:
        request_id =  data["request_id"]
        group_id=  data["group_id"]
        seller = 0
        valid = data["valid"]
        json_data = {
            "request_id": request_id,
            "group_id": group_id,
            "seller": seller,
            "valid": valid
        }
        response = requests.post(os.getenv("API_URL")+"/update_ticket/", json=json_data)
    except Exception as e:
        print("Error al manejar el mensaje:", e)
    pass
>>>>>>> 459eea5 (Ticket model, mqtt non funcional)
