from classes.flightsBD import flightsBD
from functions.flights import *
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from classes.user import User

console = Console()

def user_panel(user):
    poprawnosc = False
    choice = 0
    print("\n===================================")
    print(f"✈️ Welcome, {user.first_name} {user.last_name}!")
    print("===================================\n")
    
    while not poprawnosc:
        flights = load_flights(file_path_airplanes="data/airplanes.txt", file_path_flights="data/flight.txt")
        FlightsBD = flightsBD(flights)
        
        print("Here are the options available to you:\n")
        print("1️⃣  View tabletime of flights")
        print("2️⃣  View available flights")
        print("3️⃣  Book a flight")
        print("4️⃣  Cancel a flight")
        print("5️⃣  View my bookings")
        print("6️⃣  Search connections (from → to)")
        print("7️⃣  Loyalty program / View points")
        print("8️⃣  Change personal information")
        print("9️⃣  Log out")
        print("🔟 Exit\n")
        
        print("Please select an option by entering the number.\n")
        print("===================================\n")
        
        try:
            choice = int(input("Your choice: "))
            if 1>=choice>=9:
                print("Please enter a number between 1 and 10")
        except ValueError:
            print("Please enter a number between 1 and 10")

        if choice == 1:
            console.print(Panel.fit("[bold cyan]Timetable[/bold cyan]", border_style="cyan")) 
            FlightsBD.timetable()
            input("Press Enter to return to the panel...")
        elif choice == 2:
            console.print(Panel.fit("[bold cyan]Available flights[/bold cyan]", border_style="cyan"))
            FlightsBD.showInformation()
            input("Press Enter to return to the panel...")
        elif choice == 3:
            console.print(Panel.fit("[bold magenta]Book a flight[/bold magenta]", border_style="bright_magenta"))
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
                            bf.write(';'.join([str(user.id), str(matched.id), matched.origin, matched.destination, str(matched.distance), str(matched.duration),str(matched.ticketPrice),str(matched.points),airplane_name]) + '\n')
                        console.print(Panel.fit(f"[bold green]Booking saved for {matched.origin} → {matched.destination}[/bold green]", border_style="green"))
                    except Exception as e:
                        console.print(f"[red]Could not save booking: {e}[/red]")
                else:
                    console.print("[red]No matching flight found for that route.[/red]")
        elif choice == 4:
            console.print(Panel.fit("[bold cyan]Cancel fLight [/bold cyan]", border_style="cyan"))
            input("Press Enter to return to the panel...")
        elif choice == 5:
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
        elif choice == 6:
            console.print(Panel.fit("[bold cyan]Search connections[/bold cyan]", border_style="cyan"))
            input("Press Enter to return to the panel...")
        elif choice == 7:
            console.print(Panel.fit("[bold cyan]Loyalty program / View points[/bold cyan]", border_style="cyan"))
            input("Press Enter to return to the panel...")
        elif choice == 8:
            console.print(Panel.fit("[bold cyan]Change personal information[/bold cyan]", border_style="cyan"))
            user.chnageInformation("data/users.txt")
            input("Press Enter to return to the panel...")
        elif choice == 9:
            console.print(Panel.fit("[bold cyan]Logout[/bold cyan]", border_style="cyan")) 
            return "logout"
        elif choice == 10:
            console.print(Panel.fit("[bold cyan]Exit[/bold cyan]", border_style="cyan")) 
            console.print("\n👋 [bold yellow]Goodbye![/bold yellow]")
            return "exit"
        