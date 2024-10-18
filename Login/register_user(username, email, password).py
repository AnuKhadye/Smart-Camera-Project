# Written by Fernando Campos on 30/03/2024

import sqlite3
import bcrypt
import re  # For regular expressions

def validate_username(username):
  if len(username) < 6:
    raise ValueError("Username must be at least 6 characters long.")
  # You can add other username validation rules here (e.g., special characters)

def validate_email(email):
  email_regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$"
  if not re.match(email_regex, email):
    raise ValueError("Invalid email address.")
  # You can add other email validation rules here (e.g., domain name checks)

def register_user(username, email, password):
  # Connect to your database
  conn = sqlite3.connect('Users_Login_Images_Outcome.db')
  cursor = conn.cursor()

  try:
    # Check for empty fields
    if not username or not email or not password:
      raise ValueError("Username, email, and password cannot be empty.")

    # Validate username and email (optional, but recommended)
    validate_username(username)
    validate_email(email)

    # Check for duplicate username (assuming username is unique)
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
      raise ValueError("Username already exists. Please choose a different one.")

    # Hash password before storing (replace with a secure hashing algorithm like bcrypt)
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Insert new user into database with secure password
    cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()

    # Welcome message upon successful registration
    print("Welcome to the Maverick Smart Camera!")

    # Success message
    print("User registration successful!")

  except ValueError as e:
    print(f"Error: {e}")  # Informative error message

  finally:
    cursor.close()
    conn.close()

def login_user(username, password):
  # Connect to your database
  conn = sqlite3.connect('Users_Login_Images_Outcome.db')
  cursor = conn.cursor()

  try:
    # Check for empty fields
    if not username or not password:
      raise ValueError("Username and password cannot be empty.")

    # Query for the user with the provided username
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
      raise ValueError("Invalid username or password.")

    # Hash the entered password and compare with stored hash
    entered_password_hash = bcrypt.hashpw(password.encode(), user[3])  # Assuming password_hash is at index 3

    if entered_password_hash != user[3]:  # Compare hashed passwords
      raise ValueError("Invalid username or password.")

    # Login successful message
    print(f"Welcome back, {user[1]}!")  # Assuming username is at index 1

  except ValueError as e:
    print(f"Error: {e}")  # Informative error message

  finally:
    cursor.close()
    conn.close()

# Main execution block with login functionality integrated
if __name__ == '__main__':
  while True:
    print("Welcome! Please choose an option:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
      username = input("Enter username: ")
      email = input("Enter email: ")
      password = input("Enter password: ")
      register_user(username, email, password)
    elif choice == '2':
      username = input("Enter username: ")
      password = input("Enter password: ")
      login_user(username, password)
    elif choice == '3':
      print("Exiting...")
      break
    else:
      print("Invalid choice. Please try again.")
