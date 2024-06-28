import requests
import json
import os

local_group_id = 23

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
        
        response = requests.post(os.getenv("API_URL")+"/flights/", json=flight_json) 
        if response.status_code == 200:
            print("Mensaje enviado a la API con éxito.")
        else:
            print("Error al enviar el mensaje a la API:", response.text)
    except json.JSONDecodeError as e:
        print("Error al decodificar el mensaje JSON:", e)
    except requests.exceptions.RequestException as e:
        print("Error al enviar el mensaje a la API:", e)

def handleTicketValidation(data):
    try:
        request_id =  data["request_id"]
        group_id=  data["group_id"]
        seller = 0
        valid = data["valid"]
        json_data = {
            "request_id": request_id,
            "group_id": group_id,
            "seller": seller,
            "valid": "valid" if valid else "invalid"
        }
        if group_id == local_group_id:
            response = requests.patch(os.getenv("API_URL")+"/tickets/", json=json_data)
            if response.status_code == 200:
                print("Mensaje enviado a la API con éxito.")
            else:
                print("Error al enviar el mensaje a la API:", response.text)
        else:
            print("Validacion para otro grupo")
    except Exception as e:
        print("Error al manejar el mensaje:", e)
    pass

def handleAuction(data):
    try:
        auction_id = data["auction_id"]
        proposal_id = data["proposal_id"]
        departure_airport = data["departure_airport"]
        arrival_airport = data["arrival_airport"]
        departure_time = data["departure_time"]
        airline = data["airline"]
        quantity = data["quantity"]
        group_id = data["group_id"]
        type = data["type"]

        auction_json = {
            "auction_id": auction_id,
            "proposal_id": proposal_id,
            "departure_airport": departure_airport,
            "arrival_airport": arrival_airport,
            "departure_time": departure_time,
            "airline": airline,
            "quantity": quantity,
            "group_id": group_id,
            "type": type
        }
        response = requests.post(os.getenv("API_URL")+"/auctions/", json=auction_json)
        if response.status_code == 200:
            print("Mensaje enviado a la API con éxito.")
        else:
            print("Error al enviar el mensaje a la API:", response.text)
    except Exception as e:
        print("Error al manejar el mensaje:", e)
    pass