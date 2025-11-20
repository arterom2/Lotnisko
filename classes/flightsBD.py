from rich.table import Table
from rich.console import Console
from datetime import timedelta

class flightsBD():
    def __init__(self, fights):
        self.fights = fights

    def __str__(self):
        for i in range(0, len(self.fights)):
            return f"Flight {self.fights[i].origin} -> {self.fights[i].destination}, departure: {self.fights[i].departure.strftime('%Y-%m-%d %H:%M')}, distance: {self.fights[i].distance} km, duration: {self.fights[i].duration} h, price: {self.fights[i].ticketPrice}, points: {self.fights[i].points}, airplane: {self.fights[i].airplane.name} {self.fights[i].airplane.model}, seats {self.fights[i].takenSeats}/{self.fights[i].airplane.seatsQuantity}"
            
    def showInformation(self):
        console = Console()
        table = Table(title="Available Flights")

        table.add_column("From", style="cyan", no_wrap=True)
        table.add_column("To", style="cyan", no_wrap=True)
        table.add_column("Departure", style="cyan")
        table.add_column("Distance (km)", justify="right")
        table.add_column("Duration (h)", justify="right")
        table.add_column("Price ($)", justify="right")
        table.add_column("Points", justify="right")
        table.add_column("Airplane", style="magenta")
        table.add_column("Seats (taken/all)", style="green")

        for flight in self.fights:
            if(flight.takenSeats < flight.airplane.seatsQuantity):
                airplane_name = f"{flight.airplane.name} {flight.airplane.model}" if flight.airplane else "Unknown"
                seats = f"{flight.takenSeats}/{flight.airplane.seatsQuantity}"
                table.add_row(
                    flight.origin,flight.destination,str(flight.departure.strftime("%Y-%m-%d %H:%M")),str(flight.distance),str(flight.duration),str(flight.ticketPrice),str(flight.points),airplane_name,seats
                )
        console.print(table)
        
    def timetable(self):
        odloty = []
        przyloty = []
        for flight in self.fights:
            if(flight.origin.lower() == "poznan"):
                odloty.append(flight)
            elif(flight.destination.lower() == "poznan"):
                przyloty.append(flight)
                
        console = Console()
        table1 = Table(title="Arivals")
        table2 = Table(title="Departures")
        
        table1.add_column("From", style="cyan", no_wrap=True)
        table1.add_column("To", style="cyan", no_wrap=True)
        table1.add_column("Departure", style="cyan")
        table1.add_column("Distance (km)", justify="right")
        table1.add_column("Duration (h)", justify="right")
        table1.add_column("Airplane", style="magenta")
                
        table2.add_column("From", style="cyan", no_wrap=True)
        table2.add_column("To", style="cyan", no_wrap=True)
        table2.add_column("Departure", style="cyan")
        table2.add_column("Distance (km)", justify="right")
        table2.add_column("Duration (h)", justify="right")
        table2.add_column("Airplane", style="magenta")
        
        for flight in odloty:
            airplane_name = f"{flight.airplane.name} {flight.airplane.model}" if flight.airplane else "Unknown"
            table2.add_row(
                flight.origin,flight.destination,str(flight.departure.strftime("%Y-%m-%d %H:%M")),str(flight.distance),str(flight.duration),airplane_name
            )
        console.print(table2)
        
        for flight in przyloty:
            airplane_name = f"{flight.airplane.name} {flight.airplane.model}" if flight.airplane else "Unknown"
            arrival_time = flight.departure + timedelta(hours=flight.duration)
            table1.add_row(
                flight.origin,flight.destination,str(arrival_time.strftime("%Y-%m-%d %H:%M")),str(flight.distance),str(flight.duration),airplane_name
            )
        console.print(table1)