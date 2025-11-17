from classes.flightsBD import flightsBD
from functions.flights import *

def user_panel(user):
    poprawnosc = False
    choice = 0
    print("\n===================================")
    print(f"✈️ Welcome, {user.first_name} {user.last_name}!")
    print("===================================\n")
    
    flights = load_flights(file_path_airplanes="data/airplanes.txt", file_path_flights="data/flight.txt")
    FlightsBD = flightsBD(flights)
    
    while not poprawnosc:
        print("Here are the options available to you:\n")
        print("1️⃣  View tabletime of flights")
        print("2️⃣  View available flights")
        print("3️⃣  Book a flight")
        print("4️⃣  Cancel a flight")
        print("5️⃣  Change personal information")
        print("6️⃣  Loyalty program / View points")
        print("7️⃣  Search connections (from → to)")
        print("8️⃣  Logout / Exit\n")
        
        print("Please select an option by entering the number.\n")
        print("===================================\n")
        
        try:
            choice = int(input("Your choice: "))
            if 1>=choice>=7:
                print("Please enter a number between 1 and 7")
        except ValueError:
            print("Please enter a number between 1 and 7")

        if choice == 1:
            print("Tabletime of flights")
            FlightsBD.timetable()
        elif choice == 2:
            print("View available flights")
            FlightsBD.showInformation()
        elif choice == 3:
            print("Book a flight")
        elif choice == 4:
            print("Cancel a flight")
        elif choice == 5:
            print("Change personal information")
        elif choice == 6:
            print("Loyalty program / View points")
        elif choice == 7:
            print("Search connections")
        elif choice == 8:
            print("Logout / Exit")
            poprawnosc = True