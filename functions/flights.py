from utils.file_handler import load_data, save_data
from classes.airplane import Airplane
from classes.flight import Flight
from datetime import datetime

def load_airplanes(file_path):
    airplanes = []
    data = load_data(file_path)
    for row in data:
        id,name,model,capacity,distance = row
        airplanes.append(Airplane(int(id),name,model,int(capacity), int(distance.strip())))
    return airplanes
                
        
def load_flights(file_path_flights, file_path_airplanes):
    flights = []
    airplanes = load_airplanes(file_path_airplanes)
    data = load_data(file_path_flights)
    for row in data:
        idFlight, idAirplane, origin, destination, distance, duration, ticketPrice, points, takenSeats, departure_str = row
        departure = datetime.fromisoformat(departure_str.strip())
        airplane = next((a for a in airplanes if a.id == int(idAirplane)),None)
        flights.append(Flight(int(idFlight), airplane, origin, destination,float(distance), float(duration), float(ticketPrice), int(points.strip()), int(takenSeats),departure))
    return flights