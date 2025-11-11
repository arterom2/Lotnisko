from classes.user import User
from utils.file_handler import load_data, save_data


def load_users(file_path):
    users = []
    data = load_data(file_path)
    for row in data:
        id, login, password, first_name, last_name, role = row
        users.append(User(id, login, password, first_name, last_name, role))
    return users


def login(users):
    print("=== LOG IN ===")
    login_input = input("Login: ")
    password_input = input("Password: ")

    for u in users:
        if u.login == login_input and u.password == password_input:
            print(f"\n✅ Logged in as {u.first_name} {u.last_name} \n")
            return u

    print("\n❌ Invalid login or password!\n")
    return None


def register(users, file_path):
    print("=== REGISTER ===")
    login_input = input("Login: ")
    password_input = input("Password: ")
    password_confirm = input("Confirm Password: ")


    for u in users:
        if u.login == login_input:
            print("❌ This login already exists!\n")
            return users
        
    while True:
        if password_input != password_confirm:
            print("❌ Passwords do not match! Please try again.")
            password_input = input("Password: ")
            password_confirm = input("Confirm Password: ")
        else:
            break

    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    new_id = str(len(users) + 1)
    new_user = User(new_id, login_input, password_input, first_name, last_name, "0")
    users.append(new_user)

    data = load_data(file_path)
    data.append([new_id, login_input, password_input, first_name, last_name, "0"])
    save_data(file_path, data)

    print(f"\n✅ User {first_name} {last_name} registered successfully with role 0!\n")
    return users


def greeting(file_path='data/users.txt'):
    users = load_users(file_path)

    while True:
        print("===================================")
        print("   Welcome to the Airport Portal   ")
        print("===================================\n")
        print("1. Log in")
        print("2. Register")
        print("3. Exit")

        choice = input("\nPlease select an option (1-3): ")

        if choice == '1':
            user = login(users)
            if user:
                return user
        elif choice == '2':
            users = register(users, file_path)
        elif choice == '3':
            print("Goodbye!")
            return None
        else:
            print("❌ Invalid option. Please try again.\n")
