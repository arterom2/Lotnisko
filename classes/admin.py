from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from datetime import datetime, timedelta
from functions.flights import load_flights
from utils.file_handler import load_data, save_data
from classes.flight import Flight

class Admin:
    def __init__(self, id, login, password, first_name, last_name, role):
        self.id = id
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.role = role

    def showInformation(self):
        console = Console()
        info = (
            f"[bold cyan]Login:[/bold cyan] {self.login}\n"
            f"[bold cyan]First Name:[/bold cyan] {self.first_name}\n"
            f"[bold cyan]Last Name:[/bold cyan] {self.last_name}\n"
            f"[bold cyan]Role:[/bold cyan] {self.role}"
        )
        console.print(Panel(info, title="Admin Information", border_style="bright_blue"))

    def add_flight(self, FlightsBD):
        console = Console()
        console.print(Panel.fit("[bold cyan]Add a New Flight[/bold cyan]", border_style="cyan"))

        try:
            flight_data = load_data("data/flight.txt")
            if flight_data:
                last_id = max(int(row[0]) for row in flight_data)
                flight_id = str(last_id + 1)
            else:
                flight_id = "1"

            origin = Prompt.ask("[bold yellow]Enter origin[/bold yellow]")
            destination = Prompt.ask("[bold yellow]Enter destination[/bold yellow]")
            distance = FloatPrompt.ask("[bold yellow]Enter distance (km)[/bold yellow]")
            duration = FloatPrompt.ask("[bold yellow]Enter duration (h)[/bold yellow]")
            price = FloatPrompt.ask("[bold yellow]Enter ticket price[/bold yellow]")
            points = IntPrompt.ask("[bold yellow]Enter loyalty points[/bold yellow]")
            takenSeats = 0
            departure_str = Prompt.ask("[bold yellow]Enter departure time (YYYY-MM-DD HH:MM)[/bold yellow]")
            departure = datetime.strptime(departure_str, "%Y-%m-%d %H:%M")

            airplane_name = Prompt.ask("[bold yellow]Enter airplane name (e.g., Airbus)[/bold yellow]").strip()
            airplane_model = Prompt.ask("[bold yellow]Enter airplane model (e.g., A380)[/bold yellow]").strip()

            airplane = None
            for f in FlightsBD.fights:
                a = f.airplane
                if a.name.lower() == airplane_name.lower() and a.model.lower() == airplane_model.lower():
                    airplane = a
                    break

            if airplane is None:
                console.print(f"[red]Airplane {airplane_name} {airplane_model} not found![/red]")
                return

            new_flight = Flight(int(flight_id), airplane, origin, destination, distance, duration, price, points, takenSeats, departure)
            FlightsBD.fights.append(new_flight)

            file_data = load_data("data/flight.txt")
            file_data.append([
                flight_id,
                str(airplane.id),
                origin,
                destination,
                str(distance),
                str(duration),
                str(price),
                str(points),
                str(takenSeats),
                departure.isoformat()
            ])
            save_data("data/flight.txt", file_data)

            console.print(Panel.fit(
                f"[bold green]Flight {origin} -> {destination} added successfully![/bold green]\n"
                f"[bold cyan]Flight ID:[/bold cyan] {flight_id}, [bold cyan]Airplane:[/bold cyan] {airplane.name} {airplane.model}",
                border_style="green"
            ))

        except Exception as e:
            console.print(f"[red]Error adding flight: {e}[/red]")

    def edit_flight(self, FlightsBD):
        console = Console()
        if not FlightsBD.fights:
            console.print(Panel.fit("[red]No flights available to edit.[/red]", border_style="red"))
            return

        console.print(Panel.fit("[bold cyan]Available Flights[/bold cyan]", border_style="cyan"))
        for idx, f in enumerate(FlightsBD.fights, start=1):
            console.print(f"{idx}. ID: {f.id} | {f.origin} -> {f.destination} | Departure: {f.departure.strftime('%Y-%m-%d %H:%M')} | Airplane: {f.airplane.name} {f.airplane.model}")

        flight_idx = int(input("Enter the number of the flight you want to edit: ")) - 1
        if flight_idx < 0 or flight_idx >= len(FlightsBD.fights):
            console.print("[red]Invalid flight number![/red]")
            return
        flight = FlightsBD.fights[flight_idx]

        fields = [
            ("Origin", "origin"),
            ("Destination", "destination"),
            ("Distance (km)", "distance"),
            ("Duration (h)", "duration"),
            ("Ticket Price", "ticketPrice"),
            ("Loyalty Points", "points"),
            ("Departure (YYYY-MM-DD HH:MM)", "departure")
        ]

        while True:
            console.print("\nWhich field do you want to edit?")
            for i, (name, _) in enumerate(fields, start=1):
                console.print(f"{i}. {name}")
            console.print(f"{len(fields)+1}. Done editing")

            choice = int(input("Enter number of field to edit: "))
            if choice == len(fields)+1:
                break
            elif choice < 1 or choice > len(fields):
                console.print("[red]Invalid choice![/red]")
                continue

            field_name, attr_name = fields[choice-1]

            if attr_name in ["distance", "duration", "ticketPrice"]:
                new_val = float(input(f"Enter new {field_name}: "))
            elif attr_name == "points":
                new_val = int(input(f"Enter new {field_name}: "))
            elif attr_name == "departure":
                while True:
                    val = input(f"Enter new {field_name}: ")
                    try:
                        new_val = datetime.strptime(val, "%Y-%m-%d %H:%M")
                        break
                    except ValueError:
                        console.print("[red]Invalid date format! Use YYYY-MM-DD HH:MM[/red]")
            else:
                new_val = input(f"Enter new {field_name}: ")

            setattr(flight, attr_name, new_val)

            file_data = load_data("data/flight.txt")
            for row in file_data:
                if int(row[0]) == flight.id:
                    col_index_map = {
                        "origin": 2,
                        "destination": 3,
                        "distance": 4,
                        "duration": 5,
                        "ticketPrice": 6,
                        "points": 7,
                        "departure": 9
                    }
                    row[col_index_map[attr_name]] = new_val.isoformat() if attr_name == "departure" else str(new_val)
                    break
            save_data("data/flight.txt", file_data)

            try:
                bookings = load_data("data/bookings.txt")
                col_map = {
                    "origin": 2,
                    "destination": 3,
                    "distance": 4,
                    "duration": 5,
                    "ticketPrice": 6,
                    "points": 7,
                    "departure": 9
                }
                for b in bookings:
                    if int(b[1]) == flight.id:
                        value = new_val.isoformat() if attr_name == "departure" else str(new_val)
                        b[col_map[attr_name]] = f"{value} (changed)"
                save_data("data/bookings.txt", bookings)
            except Exception as e:
                console.print(f"[red]Error updating bookings: {e}[/red]")

            console.print(f"[green]{field_name} updated successfully![/green]")

        console.print(Panel.fit(f"[bold green]Editing of flight ID {flight.id} completed![/bold green]", border_style="green"))
        
    def chnageInformation(self, file_path):
        from functions.auth import load_users, save_data
        console = Console()
        self.showInformation()

        while True:
            console.print("[bold cyan]1.[/bold cyan] Change first name")
            console.print("[bold cyan]2.[/bold cyan] Change last name")
            console.print("[bold cyan]3.[/bold cyan] Change password")
            console.print("[bold cyan]4.[/bold cyan] Back\n")
            
            try:
                choice = int(input("Your choice: "))
                if 1>=choice>=3:
                    print("Please enter a number between 1 and 4")
            except ValueError:
                print("Please enter a number between 1 and 4")
                
            if choice == 1:
                new_name = input("Enter new first name: ")
                self.first_name = new_name
                console.print("[green]First name updated![/green]")   
            elif choice == 2:
                new_last = input("Enter new last name: ")
                self.last_name = new_last
                console.print("[green]Last name updated![/green]")
            elif choice == 3:
                attempts = 0
                max_attempts = 3
                while attempts < max_attempts:
                    old_pass = input("Enter current password: ")
                    if old_pass != self.password:
                        console.print(f"[red]Wrong password! Attempts left: {max_attempts - attempts}[/red]")
                        attempts+=1
                    else:
                        new_pass = input("Enter new password: ")
                        self.password = new_pass
                        console.print("[green]Password updated![/green]")
                        break
                else:
                    console.print("[red]Too many incorrect attempts. Returning to menu.[/red]")
            elif choice == 4:
                return
            else:
                console.print("[red]Invalid option.[/red]")


            users = load_users(file_path)
            new_data = []
            for u in users:
                if u.id == self.id:
                    new_data.append([self.id, self.login, self.password, self.first_name, self.last_name, self.role, 0])
                else:
                    new_data.append([u.id, u.login, u.password, u.first_name, u.last_name, u.role, u.loyalty_points])
            save_data(file_path, new_data)
            self.showInformation()
            
    def cancel_flight(self, FlightsDB):
        from utils.file_handler import load_data, save_data
         
        console = Console()
        
        console.print(Panel.fit("[bold cyan]Available Flights[/bold cyan]", border_style="cyan"))
        console = Console()
        table = Table(title="Available Flights")

        table.add_column("ID", style="blue")
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
        FlightsDB.fights.sort(key=lambda f: f.departure)
        
        for flight in FlightsDB.fights:
            if flight.airplane:
                airplane_name = f"{flight.airplane.name} {flight.airplane.model}" 
            else:
                airplane_name = "Unknown"
            seats = f"{flight.takenSeats}/{flight.airplane.seatsQuantity}"
            arrival_time = flight.departure + timedelta(hours=flight.duration)
            table.add_row(
                str(flight.id),flight.origin,flight.destination,str(flight.departure.strftime("%Y-%m-%d %H:%M")), str(arrival_time.strftime("%Y-%m-%d %H:%M")),str(flight.distance),str(flight.duration),str(flight.ticketPrice),str(flight.points),airplane_name,seats
            )
        console.print(table)
        
        while True:
            console.print("[bold cyan]1.[/bold cyan] Delete flight")
            console.print("[bold cyan]2.[/bold cyan] Back\n")

            try:
                choice = int(input("Your choice: "))
                if choice not in [1, 2]:
                    console.print("[red]Please enter 1 or 2[/red]")
                    continue
            except ValueError:
                console.print("[red]Please enter 1 or 2[/red]")
                continue

            if choice == 2:
                return

            if choice == 1:
                try:
                    flight_id = int(input("Enter flight id to delete: "))
                    flight_to_cancel = next((f for f in FlightsDB.fights if f.id == flight_id), None)
                    if not flight_to_cancel:
                        console.print("[red]This ID does not exist![/red]")
                        continue

                    FlightsDB.fights = [f for f in FlightsDB.fights if f.id != flight_id]
                    console.print("[green]Flight deleted![/green]")

                    flight_data = load_data("data/flight.txt")
                    new_flights = [f for f in flight_data if int(f[0]) != flight_to_cancel.id]
                    save_data("data/flight.txt", new_flights)

                    bookings = load_data("data/bookings.txt")
                    new_bookings = []

                    for b in bookings:
                        if len(b) < 2:
                            continue
                        flight_id_str = b[1].strip()
                        if flight_id_str.isdigit() and int(flight_id_str) == flight_to_cancel.id:
                            if len(b) < 12:
                                b.append("CANCELLED")
                            else:
                                b[-1] = "CANCELLED" 
                        new_bookings.append(b)

                    save_data("data/bookings.txt", new_bookings)

                except ValueError:
                    console.print(f"[yellow]Enter a number![/yellow]")