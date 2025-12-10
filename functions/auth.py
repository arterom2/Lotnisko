from classes.user import User
from utils.file_handler import load_data, save_data
from rich.console import Console
from rich.panel import Panel

console = Console()


def load_users(file_path):
    users = []
    data = load_data(file_path)
    for row in data:
        id, login, password, first_name, last_name, role, points = row
        points = int(points)
        users.append(User(id, login, password, first_name, last_name, role, points))
    return users


def login(users):
    console.print(Panel.fit("[bold cyan]🔐 LOG IN[/bold cyan]", border_style="bright_blue"))
    
    console.print("[yellow]Login:[/yellow]", end=" ")
    login_input = input()
    console.print("[yellow]Password:[/yellow]", end=" ")
    password_input = input()

    for u in users:
        if u.login == login_input and u.password == password_input:
            console.print(Panel(
                f"✅ Logged in as [bold green]{u.first_name} {u.last_name}[/bold green]\n"
                f"Role: [cyan]{u.role}[/cyan]",
                border_style="green"
            ))
            return u

    console.print(Panel("[bold red]❌ Invalid login or password![/bold red]", border_style="red"))
    return None


def register(users, file_path):
    console.print(Panel.fit("[bold magenta]📝 REGISTER[/bold magenta]", border_style="magenta"))

    while True:
        console.print("[yellow]Login:[/yellow]", end=" ")
        login_input = input().strip()
        if login_input == "":
            console.print("[red]Login cannot be empty. Please enter a login.[/red]")
            continue
        if any(u.login == login_input for u in users):
            console.print("[bold red]❌ This login already exists! Try another.[/bold red]")
            continue
        break

    while True:
        console.print("[yellow]Password:[/yellow]", end=" ")
        password_input = input()
        if password_input.strip() == "":
            console.print("[red]Password cannot be empty. Please enter a password.[/red]")
            continue
        console.print("[yellow]Confirm Password:[/yellow]", end=" ")
        password_confirm = input()
        if password_input != password_confirm:
            console.print("[bold red]❌ Passwords do not match! Please try again.[/bold red]")
            continue
        break

    while True:
        console.print("[yellow]First Name:[/yellow]", end=" ")
        first_name = input().strip()
        if first_name == "":
            console.print("[red]First name cannot be empty.[/red]")
            continue
        break

    while True:
        console.print("[yellow]Last Name:[/yellow]", end=" ")
        last_name = input().strip()
        if last_name == "":
            console.print("[red]Last name cannot be empty.[/red]")
            continue
        break

    new_id = str(len(users) + 1)
    new_user = User(new_id, login_input, password_input, first_name, last_name, "0", 0)
    users.append(new_user)

    data = load_data(file_path)
    data.append([new_id, login_input, password_input, first_name, last_name, "0", 0])
    save_data(file_path, data)

    console.print(Panel(
        f"✅ User [bold green]{first_name} {last_name}[/bold green] registered successfully!",
        border_style="green"
    ))
    return users


def greeting(file_path='data/users.txt'):
    users = load_users(file_path)

    while True:
        console.print(Panel.fit(
            "[bold yellow]Welcome to the Airport Portal ✈️[/bold yellow]",
            subtitle="[cyan]Select an option below[/cyan]",
            border_style="bright_blue"
        ))
        
        console.print("[bold cyan]1.[/bold cyan] Log in")
        console.print("[bold cyan]2.[/bold cyan] Register")
        console.print("[bold cyan]3.[/bold cyan] Exit\n")

        console.print("[yellow]Please select an option (1-3):[/yellow]", end=" ")
        choice = input()

        if choice == '1':
            user = login(users)
            if user:
                return user
        elif choice == '2':
            users = register(users, file_path)
        elif choice == '3':
            console.print("\n👋 [bold yellow]Goodbye![/bold yellow]")
            return None
        else:
            console.print("[bold red]❌ Invalid option. Please try again.[/bold red]\n")
