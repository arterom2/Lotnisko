from rich.console import Console
from rich.panel import Panel
from classes.flightsBD import flightsBD
from functions.flights import load_flights

console = Console()

def admin_panel(admin):
    print("\n===================================")
    print(f"🛫 Welcome Admin, {admin.first_name} {admin.last_name}!")
    print("===================================\n")

    while True:
        flights = load_flights("data/flight.txt", "data/airplanes.txt")
        FlightsBD = flightsBD(flights)

        print("Admin options:\n")
        print("1️⃣  Show all flights")
        print("2️⃣  Add a new flight")
        print("3️⃣  Cancel a flight")
        print("4️⃣  Edit a flight")
        print("5️⃣  Show admin information")
        print("6️⃣  Change personal information")
        print("7️⃣  Delete a user")
        print("8️⃣  Log out")
        print("9️⃣  Exit")
        print("\n===================================\n")

        try:
            choice = int(input("Your choice: "))
        except ValueError:
            console.print("[red]Enter a valid number.[/red]")
            continue

        if choice == 1:
            console.print(Panel.fit("[bold cyan]All Flights[/bold cyan]", border_style="cyan"))
            FlightsBD.showInformation()
            input("Press Enter to return...")

        elif choice == 2:
            admin.add_flight(FlightsBD)
            input("Press Enter to return...")

        elif choice == 3:
            admin.cancel_flight(FlightsBD)
            input("Press Enter to return...")

        elif choice == 4:
            admin.edit_flight(FlightsBD)
            input("Press Enter to return...")

        elif choice == 5:
            admin.showInformation()
            input("Press Enter to return...")

        elif choice == 6:
            console.print(Panel.fit("[bold cyan]Change personal information[/bold cyan]", border_style="cyan"))
            admin.chnageInformation("data/users.txt")
        elif choice == 7:
            admin.delete_user(file_path='data/users.txt')
            input("Press Enter to return...")

        elif choice == 8:
            console.print(Panel.fit("[bold cyan]Logout[/bold cyan]", border_style="cyan"))
            return "logout"

        elif choice == 9:
            console.print(Panel.fit("[bold cyan]Exit[/bold cyan]", border_style="cyan"))
            console.print("\n👋 [bold yellow]Goodbye![/bold yellow]")
            return "exit"

        else:
            console.print("[red]Invalid option. Try again.[/red]")
