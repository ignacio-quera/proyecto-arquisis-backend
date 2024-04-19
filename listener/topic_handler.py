import requests
import json
import os


def handleFlightInfo(data):
    try:
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
        
        response = requests.post(os.getenv("_URL")+"/create_flights/", json=flight_json) 
        if response.status_code == 200:
            print("Mensaje enviado a la API con éxito.")
        else:
            print("Error al enviar el mensaje a la API:", response.text)
    except json.JSONDecodeError as e:
        print("Error al decodificar el mensaje JSON:", e)
    except requests.exceptions.RequestException as e:
        print("Error al enviar el mensaje a la API:", e)

def handleTicketValidation(data):
    pass