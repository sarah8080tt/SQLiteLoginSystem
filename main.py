import sqlite3
import bcrypt

# Step 1: Setup SQLite database
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Step 2: Register a new user
def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Hash the password for security
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    finally:
        conn.close()
    main_menu()

# Step 3: Login an existing user
def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        print("Login successful!")
        user_dashboard()
    else:
        print("Error: Invalid username or password.")
    conn.close()
    main_menu()

# User dashboard
def user_dashboard():
    print("Welcome to your dashboard!")
    # Add more user-specific functionality here
    main_menu()

# Step 4: Main menu
def main_menu():
    print("\nMain Menu:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        register_user()
    elif choice == '2':
        login_user()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        main_menu()

# Entry point
if __name__ == '__main__':
    setup_database()
    main_menu()


