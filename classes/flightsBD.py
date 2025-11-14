from utils.file_handler import load_data, save_data
from classes.airplane import Airplane

class flightsBD():
    def __init__(self, fights):
        self.fights = fights

    def __str__(self):
        for i in range(0, len(self.fights)):
            print((f"Flight {self.fights[i].origin} -> {self.fights[i].destination}, distance: {self.fights[i].distance} km, duration: {self.fights[i].duration} h, \nprice: {self.fights[i].ticketPrice}, points: {self.fights[i].points}, airplane: {self.fights[i].airplane.name} {self.fights[i].airplane.model}"))
            
    def showInformation(self):
        for i in range(0, len(self.fights)):
            print((f"Flight {self.fights[i].origin} -> {self.fights[i].destination}, distance: {self.fights[i].distance} km, duration: {self.fights[i].duration} h, \nprice: {self.fights[i].ticketPrice}, points: {self.fights[i].points}, airplane: {self.fights[i].airplane.name} {self.fights[i].airplane.model}"))
    
    def load_airplanes(self,file_path):
        airplanes = []
        data = load_data(file_path)
        for row in data:
            id,name,model,capacity,distance = row
            airplanes.append(Airplane(int(id),name,model,int(capacity), int(distance.strip())))
            
    
    def load_flights(self,file_path):
        flights = []
        airplanes = [self.load_airplanes()]
        data = load_data(file_path)
        for row in data:
            idFlight, idAirplane, origin, destination, distance, duration, ticketPrice, points = data
            airplane = [a for a in airplanes if a.id == idAirplane]
            flights.append(int(idFlight), airplane, origin,destination, duration, ticketPrice, points.strip())
