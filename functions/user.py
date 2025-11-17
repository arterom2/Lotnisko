from classes.flightsBD import flightsBD
from functions.flights import *
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def user_panel(user):
    poprawnosc = False
    choice = 0
    print("\n===================================")
    print(f"✈️ Welcome, {user.first_name} {user.last_name}!")
    print("===================================\n")
    
    while not poprawnosc:
        print("Here are the options available to you:\n")
        print("1️⃣  View available flights")
        print("2️⃣  Book a flight")
        print("3️⃣  Cancel a flight")
        print("4️⃣  Change personal information")
        print("5️⃣  Loyalty program / View points")
        print("6️⃣  Search connections (from → to)")
        print("7️⃣  Logout / Exit")
        print("9️⃣  View my bookings\n")
        
        print("Please select an option by entering the number.\n")
        print("===================================\n")
        
        try:
            choice = int(input("Your choice: "))
            if 1<=choice<=9:
                poprawnosc = True
            else:
                print("Please enter a number between 1 and 9")
        except ValueError:
            print("Please enter a number between 1 and 9")

    if choice == 1:
        console.print(Panel.fit("[bold cyan]Available flights[/bold cyan]", border_style="cyan"))
        flights = load_flights(file_path_airplanes="data/airplanes.txt", file_path_flights="data/flight.txt")
        FlightsBD = flightsBD(flights)
        FlightsBD.showInformation()
    elif choice == 2:
        console.print(Panel.fit("[bold magenta] BOOK A FLIGHT[/bold magenta]", border_style="bright_magenta"))
        flights = load_flights(file_path_airplanes="data/airplanes.txt", file_path_flights="data/flight.txt")
        FlightsBD = flightsBD(flights)
        FlightsBD.showInformation()
        flight_to_book = input("\nEnter the flight (Origin - Destination) you want to book: ")
        parts = flight_to_book.split('-')
        if len(parts) != 2:
            console.print("[red]Please enter in format 'Origin - Destination' (e.g. Paris - London).[/red]")
        else:
            origin = parts[0].strip()
            destination = parts[1].strip()
            matched = None
            for f in flights:
                if f.origin.lower() == origin.lower() and f.destination.lower() == destination.lower():
                    matched = f
                    break

            if matched:
                table = Table.grid()
                table.add_column()
                table.add_column()
                table.add_row("From:", f"[cyan]{matched.origin}[/cyan]")
                table.add_row("To:", f"[cyan]{matched.destination}[/cyan]")
                table.add_row("Distance:", f"{matched.distance} km")
                table.add_row("Duration:", f"{matched.duration} h")
                table.add_row("Price:", f"${matched.ticketPrice}")
                table.add_row("Points:", f"{matched.points}")
                airplane_name = f"{matched.airplane.name} {matched.airplane.model}" if matched.airplane else "Unknown"
                table.add_row("Airplane:", f"[magenta]{airplane_name}[/magenta]")

                console.print(Panel(table, title="Booking confirmation", border_style="green"))

                try:
                    with open('data/bookings.txt', 'a', encoding='utf-8') as bf:
                        bf.write(';'.join([
                            str(user.id),
                            str(matched.id),
                            matched.origin,
                            matched.destination,
                            str(matched.distance),
                            str(matched.duration),
                            str(matched.ticketPrice),
                            str(matched.points),
                            airplane_name
                        ]) + '\n')
                    console.print(Panel.fit(f"[bold green]Booking saved for {matched.origin} → {matched.destination}[/bold green]", border_style="green"))
                except Exception as e:
                    console.print(f"[red]Could not save booking: {e}[/red]")
            else:
                console.print("[red]No matching flight found for that route.[/red]")

    elif choice == 3:
        print("Cancel a flight")
    elif choice == 4:
        print("Change personal information")
    elif choice == 5:
        print("Loyalty program / View points")
    elif choice == 6:
        print("Search connections")
    elif choice == 7:
        print("Logout / Exit")
    elif choice == 9:
        console.print(Panel.fit("[bold cyan] My Bookings [/bold cyan]", border_style="cyan"))
        bookings = []
        try:
            with open('data/bookings.txt', 'r', encoding='utf-8') as bf:
                for line in bf:
                    parts = line.strip().split(';')
                    if len(parts) >= 2 and parts[0] == str(user.id):
                        bookings.append(parts)
        except FileNotFoundError:
            bookings = []

        if not bookings:
            console.print("[yellow]You have no bookings.[/yellow]")
            input("Press Enter to return to the panel...")
        else:
            table = Table(title="Your Bookings")
            table.add_column("From", style="cyan")
            table.add_column("To", style="cyan")
            table.add_column("Distance")
            table.add_column("Duration")
            table.add_column("Price")
            table.add_column("Points")
            table.add_column("Airplane")

            for b in bookings:
                origin = b[2] if len(b) > 2 else ""
                destination = b[3] if len(b) > 3 else ""
                distance = b[4] if len(b) > 4 else ""
                duration = b[5] if len(b) > 5 else ""
                price = b[6] if len(b) > 6 else ""
                points = b[7] if len(b) > 7 else ""
                airplane = b[8] if len(b) > 8 else ""
                table.add_row(origin, destination, distance, duration, price, points, airplane)

            console.print(table)
            input("Press Enter to return to the panel...")