from rich.console import Console
from rich.panel import Panel

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
                    