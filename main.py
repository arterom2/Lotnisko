from functions.auth import greeting
from functions.user import user_panel


def main():
    user = greeting() 

    if user is None:
        return

    if user.role == "1":
        print(f"🔧 Welcome, {user.first_name} {user.last_name}!")
    elif user.role == "0":
        user_panel(user)
    else:
        print(f"Unknown role for {user.first_name} {user.last_name}.")

if __name__ == "__main__":
    main()