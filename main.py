from functions.auth import greeting
from functions.user import user_panel
from rich.console import Console
from rich.panel import Panel
from functions.admin import admin_panel


console = Console()
def main():
    while True:
        user = greeting() 

        if user is None:
            return

        if user.role == "1":
            print(f"🔧 Welcome, {user.first_name} {user.last_name}!")
            admin_panel(user)
        elif user.role == "0":
            result = user_panel(user)
            if result == "logout":
                continue
            elif result == "exit":
                break
        else:
            print(f"Unknown role for {user.first_name} {user.last_name}.")

if __name__ == "__main__":
    main()