from classes.flightsBD import *
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
              user.book_flight(flights, FlightsBD)
        elif choice == 4:
            console.print(Panel.fit("[bold cyan]Cancel fLight [/bold cyan]", border_style="cyan"))
            input("Press Enter to return to the panel...")
        elif choice == 5:
             user.view_bookings()
        elif choice == 6:
            console.print(Panel.fit("[bold cyan]Search connections[/bold cyan]", border_style="cyan"))
            FlightsBD.search_connections()
            input("Press Enter to return to the panel...")
        elif choice == 7:
            console.print(Panel.fit("[bold cyan]Loyalty program / View points[/bold cyan]", border_style="cyan"))
            user.ViewPoints()
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
        