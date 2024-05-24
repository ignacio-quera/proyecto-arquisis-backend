# from celery import Celery
from celery import shared_task
import math

def haversine(lat1, lon1, lat2, lon2):
    # Calculate the great circle distance between two points 
    # on the earth (specified in decimal degrees)
    # convert decimal degrees to radians 
    R = 6371  # Radius of the earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    km = R * c
    return km

@shared_task
def flight_prediction(data):
    flight_details = data["flight_details"]
    print(flight_details)
    user_coordinates = data["user_location"]

#     Se calculan la distancia de todos los vuelos encontrados en el punto anterior
# ( flight_coord ) con respecto a la ubicación de la dirección ip del usuario ( ip_coord ), y se
# ordenan en base al precio y distancia según la siguiente fórmula:
# 6. Se obtienen los 3 vuelos con los mejores ponderadores y se los muestran al usuario
# Siendo el vector de latitud y longitud de la ip del usuario, el vector de
# latitud y longitud del aeropuerto de destino de un vuelo obtenido, y el precio de ese
# vuelo.

    results = []
    id_results = []
    user_lat = float(user_coordinates["latitude"])
    user_lon = float(user_coordinates["longitude"])

    for flight in flight_details:
        print(flight)
        flight_lat = float(flight["coordinates"][0])
        flight_lon = float(flight["coordinates"][1])
        print("calculando distancia")
        distance = haversine(user_lat, user_lon, flight_lat, flight_lon)
        print(distance)
        price = flight['price']
        
        # Calcular ponderación
        score = distance/price
        print(score)

        results.append({
            'flight_id': flight['flight_id'],
            'distance': distance,
            'price': price,
            'score': score
        })
    print(results)

    # Sort flights by score
    results.sort(key=lambda x: x['score'])

    print("sorted results")
    print(results)
    
    # Return the top 3 flights
    top_flights = results[-3:]
    print("top flights list")
    print(top_flights)
    print(type(top_flights))
    for flight in top_flights:
        id_results.append(flight['flight_id'])
    print(id_results)
    
    return id_results  