from rich.table import Table
from rich.console import Console
from datetime import timedelta, datetime

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
        table.add_column("Arrival", style="cyan")
        table.add_column("Distance (km)", justify="right")
        table.add_column("Duration (h)", justify="right")
        table.add_column("Price ($)", justify="right")
        table.add_column("Points", justify="right")
        table.add_column("Airplane", style="magenta")
        table.add_column("Seats (taken/all)", style="green")
        self.fights.sort(key=lambda f: f.departure)
        for flight in self.fights:
            if(flight.takenSeats < flight.airplane.seatsQuantity):
                if flight.airplane:
                    airplane_name = f"{flight.airplane.name} {flight.airplane.model}" 
                else:
                    airplane_name = "Unknown"
                seats = f"{flight.takenSeats}/{flight.airplane.seatsQuantity}"
                arrival_time = flight.departure + timedelta(hours=flight.duration)
                table.add_row(
                    flight.origin,flight.destination,str(flight.departure.strftime("%Y-%m-%d %H:%M")), str(arrival_time.strftime("%Y-%m-%d %H:%M")),str(flight.distance),str(flight.duration),str(flight.ticketPrice),str(flight.points),airplane_name,seats
                )
        console.print(table)
        
    def timetable(self):
        next24hours = datetime.now() + timedelta(hours=24)
        
        odloty = []
        przyloty = []
        for flight in self.fights:
            if isinstance(flight.departure, str):
                flight.departure = datetime.fromisoformat(flight.departure)
            
            if datetime.now() <= flight.departure <= next24hours:
                if(flight.origin.lower() == "poznan"):
                    odloty.append(flight)
                elif(flight.destination.lower() == "poznan"):
                    przyloty.append(flight)
                
        console = Console()
        table1 = Table(title="Arivals")
        table2 = Table(title="Departures")
        
        table1.add_column("From", style="cyan", no_wrap=True)
        table1.add_column("To", style="cyan", no_wrap=True)
        table1.add_column("Arrival", style="cyan")
        table1.add_column("Distance (km)", justify="right")
        table1.add_column("Duration (h)", justify="right")
        table1.add_column("Airplane", style="magenta")
                
        table2.add_column("From", style="cyan", no_wrap=True)
        table2.add_column("To", style="cyan", no_wrap=True)
        table2.add_column("Departure", style="cyan")
        table2.add_column("Distance (km)", justify="right")
        table2.add_column("Duration (h)", justify="right")
        table2.add_column("Airplane", style="magenta")
        

        odloty.sort(key=lambda f: f.departure)
        przyloty.sort(key=lambda f: f.departure + timedelta(hours=f.duration))

        
        for flight in odloty:
            if flight.airplane:
                airplane_name = f"{flight.airplane.name} {flight.airplane.model}" 
            else:
                airplane_name = "Unknown"
            table2.add_row(
                flight.origin,flight.destination,str(flight.departure.strftime("%Y-%m-%d %H:%M")),str(flight.distance),str(flight.duration),airplane_name
            )
        console.print(table2)
        
        for flight in przyloty:
            if flight.airplane:
                airplane_name = f"{flight.airplane.name} {flight.airplane.model}" 
            else:
                airplane_name = "Unknown"
            arrival_time = flight.departure + timedelta(hours=flight.duration)
            table1.add_row(
                flight.origin,flight.destination,str(arrival_time.strftime("%Y-%m-%d %H:%M")),str(flight.distance),str(flight.duration),airplane_name
            )
        console.print(table1)
        
        
    def searchFlights(self, origin=None, destination=None, departure_date=None, max_distance=None, airplane_brand=None):
        results = self.fights
        filtered_results = []

        if origin:
            for f in results:
                if f.origin.lower() == origin.lower():
                    filtered_results.append(f)
            results = filtered_results
            filtered_results = []

        if destination:
            for f in results:
                if f.destination.lower() == destination.lower():
                    filtered_results.append(f)
            results = filtered_results
            filtered_results = []

        if departure_date:
            for f in results:
                if f.departure.strftime("%Y-%m-%d") == departure_date:
                    filtered_results.append(f)
            results = filtered_results
            filtered_results = []

        if max_distance:
            for f in results:
                if f.distance <= max_distance:
                    filtered_results.append(f)
            results = filtered_results
            filtered_results = []

        if airplane_brand:
            for f in results:
                if airplane_brand.lower() in f.airplane.name.lower():
                    filtered_results.append(f)
            results = filtered_results

        return results
        
    def search_connections(self):
        console = Console()

        origin = console.input("[cyan]Origin[/cyan] ([grey]ENTER = skip[/grey]): ").strip()
        if not origin:
            origin = None

        destination = console.input("[cyan]Destination[/cyan] ([grey]ENTER = skip[/grey]): ").strip()
        if not destination:
            destination = None

        date = console.input("[cyan]Departure date[/cyan] ([grey]YYYY-MM-DD, ENTER = skip[/grey]): ").strip()
        if not date:
            date = None

        max_distance = console.input("[cyan]Max distance[/cyan] ([grey]ENTER = skip[/grey]): ").strip()
        if not max_distance:
            max_distance = None
        else:
            max_distance = int(max_distance)

        airplane_brand = console.input("[cyan]Airplane brand[/cyan] ([grey]ENTER = skip[/grey]): ").strip()
        if not airplane_brand:
            airplane_brand = None

        results = self.searchFlights(origin, destination, date, max_distance, airplane_brand)
        results.sort(key=lambda f: f.departure)
        if not results:
            console.print("[bold red]No flights found.[/bold red]")
            return

        table = Table(title="Search Results")
        table.add_column("ID", style="cyan")
        table.add_column("From")
        table.add_column("To")
        table.add_column("Departure")
        table.add_column("Distance")
        table.add_column("Duration")
        table.add_column("Price")
        table.add_column("Airplane")
        table.add_column("Seats")

        for f in results:
            table.add_row(
                str(f.id),
                f.origin,
                f.destination,
                f.departure.strftime("%Y-%m-%d %H:%M"),
                str(f.distance),
                str(f.duration),
                str(f.ticketPrice),
                f"{f.airplane.name} {f.airplane.model}",
                f"{f.takenSeats}/{f.airplane.seatsQuantity}",
                )
        console.print(table)