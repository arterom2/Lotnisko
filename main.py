from functions.auth import greeting
from functions.user import user_panel
from rich.console import Console
from rich.panel import Panel
from functions.admin import admin_panel
from classes.admin import Admin

console = Console()

def main():
    while True:
        user = greeting()
        if user is None:
            return

        if user.role == "1":
            admin_user = Admin(
                id=user.id,
                login=user.login,
                password=user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role
            )
            result = admin_panel(admin_user)
            if result == "logout":
                continue
            elif result == "exit":
                break

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
