from rich.table import Table
from rich.console import Console

class flightsBD():
    def __init__(self, fights):
        self.fights = fights

    def __str__(self):
        for i in range(0, len(self.fights)):
            return ((f"Flight {self.fights[i].origin} -> {self.fights[i].destination}, distance: {self.fights[i].distance} km, duration: {self.fights[i].duration} h, price: {self.fights[i].ticketPrice}, points: {self.fights[i].points}, airplane: {self.fights[i].airplane.name} {self.fights[i].airplane.model}"))
            
    def showInformation(self):
        console = Console()
        table = Table(title="Available Flights")

        table.add_column("From", style="cyan", no_wrap=True)
        table.add_column("To", style="cyan", no_wrap=True)
        table.add_column("Distance (km)", justify="right")
        table.add_column("Duration (h)", justify="right")
        table.add_column("Price ($)", justify="right")
        table.add_column("Points", justify="right")
        table.add_column("Airplane", style="magenta")

        for flight in self.fights:
            airplane_name = f"{flight.airplane.name} {flight.airplane.model}" if flight.airplane else "Unknown"
            table.add_row(
                flight.origin,flight.destination,str(flight.distance),str(flight.duration),str(flight.ticketPrice),str(flight.points),airplane_name
            )
        console.print(table)
    
    