from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime

class User:
    def __init__(self, id, login, password, first_name, last_name, role, loyalty_points):
        self.id = id
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        if(loyalty_points is not None):
            self.loyalty_points = loyalty_points
        else:
            self.loyalty_points = 0
        
    def showInformation(self):
        console = Console() 
        info = (
            f"[bold cyan]Login:[/bold cyan] {self.login}\n"
            f"[bold cyan]First Name:[/bold cyan] {self.first_name}\n"
            f"[bold cyan]Last Name:[/bold cyan] {self.last_name}\n"
            f"[bold cyan]Loyalty poins:[/bold cyan] {self.loyalty_points}"
        )
        console.print(Panel(info, title="User Information", border_style="bright_blue"))
        
    def chnageInformation(self,file_path):
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
                    new_data.append([self.id, self.login, self.password, self.first_name, self.last_name, self.role, self.loyalty_points])
                else:
                    new_data.append([u.id, u.login, u.password, u.first_name, u.last_name, u.role, u.loyalty_points])
            save_data(file_path, new_data)
            self.showInformation()
                    
                    
    def ViewPoints(self):
        console = Console()
        console.print(f"[green]{self.first_name} you have {self.loyalty_points} points!! Congratulations[/green]")
        
    def book_flight(self, flights, flightsBD, file_path="data/bookings.txt", file_path2="data/users.txt"):
        console = Console()
        console.print(Panel.fit("[bold magenta]Book a flight[/bold magenta]", border_style="magenta"))

        flightsBD.showInformation()
        flight_to_book = input("\nEnter flight (Origin - Destination): ")

        parts = flight_to_book.split('-')
        if len(parts) != 2:
            console.print("[red]Format must be: Paris - London[/red]")
            return

        origin = parts[0].strip()
        destination = parts[1].strip()
        date_input = input("Enter flight date or datetime (YYYY-MM-DD or YYYY-MM-DD HH:MM").strip()
        if date_input == "":
            console.print("[red]Date/time cannot be empty. Booking cancelled.[/red]")
            return

        import re
        matches = []
        date_norm = date_input.replace('T', ' ').strip()
        date_only_pattern = r'^\d{4}-\d{2}-\d{2}$'
        datetime_min_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$'

        for f in flights:
            f_date_only = None
            f_datetime_min = None
            f_iso = None
            f_raw = None
            try:
                if isinstance(f.departure, datetime):
                    f_date_only = f.departure.strftime('%Y-%m-%d')
                    f_datetime_min = f.departure.strftime('%Y-%m-%d %H:%M')
                    f_iso = f.departure.isoformat()
                    f_raw = f_iso
                else:
                    f_raw = str(f.departure)
                    f_raw_norm = f_raw.replace('T', ' ').strip()
                    try:
                        parsed = datetime.fromisoformat(f_raw)
                        f_date_only = parsed.strftime('%Y-%m-%d')
                        f_datetime_min = parsed.strftime('%Y-%m-%d %H:%M')
                        f_iso = parsed.isoformat()
                        f_raw = f_iso
                    except Exception:
                        parts = f_raw_norm.split(' ')
                        f_date_only = parts[0]
                        if len(parts) > 1 and ':' in parts[1]:
                            f_datetime_min = f_date_only + ' ' + parts[1][:5]
                        else:
                            f_datetime_min = f_date_only

            except Exception:
                f_raw = str(getattr(f, 'departure', ''))
                f_date_only = f_raw.split(' ')[0] if ' ' in f_raw else f_raw
                f_datetime_min = f_date_only

            if f.origin.lower() == origin.lower() and f.destination.lower() == destination.lower():
                matched_flag = False
                if re.match(date_only_pattern, date_norm):
                    if f_date_only == date_norm:
                        matched_flag = True
                elif re.match(datetime_min_pattern, date_norm):
                    if f_datetime_min == date_norm:
                        matched_flag = True
                else:
                    try:
                        inp_parsed = datetime.fromisoformat(date_input)
                        inp_iso = inp_parsed.isoformat()
                        if f_iso == inp_iso or (f_datetime_min and f_datetime_min == inp_parsed.strftime('%Y-%m-%d %H:%M')):
                            matched_flag = True
                    except Exception:
                        if f_raw == date_input or f_raw.replace('T', ' ') == date_input:
                            matched_flag = True

                if matched_flag:
                    matches.append(f)

        if not matches:
            console.print("[red]No matching flight found for that route on that date.[/red]")
            return

        if len(matches) == 1:
            matched = matches[0]
        else:
            console.print("Multiple flights found on that date:")
            for i, mf in enumerate(matches, start=1):
                try:
                    dep_str = mf.departure.strftime('%Y-%m-%d %H:%M')
                except Exception:
                    dep_str = str(mf.departure)
                console.print(f"{i}. ID:{mf.id} Departure: {dep_str} Airplane: {mf.airplane.name} {mf.airplane.model}")
            sel = input("Enter number of flight to book: ").strip()
            try:
                sel_i = int(sel)
                if 1 <= sel_i <= len(matches):
                    matched = matches[sel_i-1]
                else:
                    console.print("[red]Invalid selection. Booking cancelled.[/red]")
                    return
            except ValueError:
                console.print("[red]Invalid input. Booking cancelled.[/red]")
                return

        console.print(f"\nYou have [yellow]{self.loyalty_points}[/yellow] points.")
        while True:
            use_points = input("Do you want to use points for a discount? (yes/no): ").lower()
            if(use_points == "yes" or use_points == "no"):
                break
            else:
                console.print("[red]Your answer has to be 'yes' or 'no' [/red]")

        final_price = matched.ticketPrice
        points_used = 0

        if(use_points == "yes"):
            while True:
                try:
                    points_used = int(input("How many points do you want to use? "))
                except ValueError:
                    console.print("[red]Please enter a number.[/red]")
                    continue

                if points_used < 0:
                    console.print("[red]You cannot use negative points.[/red]")
                elif points_used > self.loyalty_points:
                    console.print("[red]You don't have that many points![/red]")
                else:
                    discount = (points_used*0.5)
                    if(discount > final_price):
                        max_discount = int(final_price/0.5)
                        console.print(f"[red]Discount cannot be higher than ticket price. Maximal amount of points you can use is {max_discount}[/red]")
                    else:
                        final_price -= discount
                        self.loyalty_points -= points_used
                        console.print(f"[green]Discount applied: {discount} zł[/green]")
                        console.print(f"[green]New price: {final_price} zł[/green]")
                        self.loyalty_points += matched.points
                        break
        else:
            self.loyalty_points += matched.points

        if not matched:
            console.print("[red]No matching flight found.[/red]")
            return

        table = Table.grid()
        table.add_column()
        table.add_column()
        table.add_row("From:", f"[cyan]{matched.origin}[/cyan]")
        table.add_row("To:", f"[cyan]{matched.destination}[/cyan]")
        table.add_row("Distance:", f"{matched.distance} km")
        table.add_row("Duration:", f"{matched.duration} h")
        table.add_row("Price:", f"${final_price}")
        table.add_row("Points:", f"{matched.points}")
        airplane_name = f"{matched.airplane.name} {matched.airplane.model}"
        table.add_row("Airplane:", f"[magenta]{airplane_name}[/magenta]")

        console.print(Panel(table, title="Booking confirmation", border_style="green"))
        
        if isinstance(matched.departure, datetime): 
            departure_str = matched.departure.isoformat() 
        else: 
            departure_str = str(matched.departure)
        
        from functions.auth import load_users, save_data   
        users = load_users(file_path2)
        new_data = []
        for u in users:
            if u.id == self.id:
                new_data.append([self.id, self.login, self.password, self.first_name, self.last_name, self.role, self.loyalty_points])
            else:
                new_data.append([u.id, u.login, u.password, u.first_name, u.last_name, u.role, u.loyalty_points])
        save_data(file_path2, new_data)
        self.showInformation()

        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(';'.join([
                    str(self.id), str(matched.id),
                    matched.origin, matched.destination,
                    str(matched.distance), str(matched.duration),
                    str(matched.ticketPrice), str(matched.points),
                    airplane_name,departure_str, " "
                ]) + "\n")
            console.print(f"[green]Booking saved! {matched.origin} → {matched.destination}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving booking: {e}[/red]")

    def view_bookings(self, file_path="data/bookings.txt"):
        from rich.console import Console
        from rich.table import Table
        console = Console()

        console.print(Panel.fit("[bold cyan]Your bookings[/bold cyan]", border_style="cyan"))

        bookings = []

        try:
            with open(file_path, 'r', encoding='utf-8') as bf:
                for line in bf:
                    parts = line.strip().split(';')
                    if len(parts) >= 2 and parts[0] == str(self.id):
                        bookings.append(parts)
        except FileNotFoundError:
            console.print("[yellow]Booking file not found.[/yellow]")
            return

        if not bookings:
            console.print("[yellow]You have no bookings.[/yellow]")
            return

        table = Table(title="Your Bookings")
        table.add_column("#", style="dim", width=4)
        table.add_column("Flight ID", style="magenta")
        table.add_column("From", style="cyan")
        table.add_column("To", style="cyan")
        table.add_column("Distance")
        table.add_column("Duration")
        table.add_column("Price")
        table.add_column("Points")
        table.add_column("Extra")
        table.add_column("Airplane")
        table.add_column("Date")
        table.add_column("Status", style="red", justify="center")

        for idx, b in enumerate(bookings, start=1):
            row = [b[i] if len(b) > i else "" for i in range(12)]
            table.add_row(
                str(idx),
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9],
                row[10],
                row[11]
            )

        console.print(table)