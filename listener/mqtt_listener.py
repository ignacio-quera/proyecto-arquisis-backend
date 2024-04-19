import paho.mqtt.client as mqtt
import time
import multiprocessing
import json
from dotenv import load_dotenv
import os
from topic_handler import handleFlightInfo, handleTicketValidation

# Especifica la ruta completa al archivo .env que deseas cargar
load_dotenv(".env", override=True) 

# Leer las credenciales desde el archivo .env
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

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

    try:
        print(f"Mensaje recibido en el tópico {msg.topic}: {msg.payload}")
        payload = msg.payload.decode()
        #Lo transformamos a un objeto de python
        data = json.loads(payload)
        topicHandlers[msg.topic](data)
    except KeyError as e:
        print(f"Error al manejar el mensaje: {e}")


# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
# client.on_connect = on_connect
# client.on_message = on_message
# client.username_pw_set(username=USER, password=PASSWORD)

# print("Conectando al broker MQTT...")
# client.connect(HOST, PORT)
# client.loop_forever()

# Función para iniciar el cliente MQTT
def start_mqtt_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.username_pw_set(username=USER, password=PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    print("Conectando al broker MQTT...")
    client.connect(HOST, PORT, keepalive=60)
    
    # Mantener el cliente MQTT en funcionamiento
    client.loop_forever()

if __name__ == "__main__":
    # Crear un proceso independiente para el cliente MQTT
    mqtt_process = multiprocessing.Process(target=start_mqtt_client)
    mqtt_process.start()

    try:
        while True:
            # Mantener el proceso principal en funcionamiento
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo el proceso MQTT...")
        mqtt_process.terminate()