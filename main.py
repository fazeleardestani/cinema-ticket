"""
This module serves as the main entry point for the user management application.

It handles the main menu, user interactions, and orchestrates calls
to the User class for registration, login, and profile management.
"""

import os
import getpass
from exeptions import InvalidPasswordError
# from models.bank import BankAccount
from models.user import User

def register_user():
    """Handles the user registration process by collecting user input."""
    os.system('cls')

    print("--- Create User ---")

    username = input("Username: ")

    print("(Your password must be at least 4 characters long.)")
    password = getpass.getpass()

    phone_number = input("Phone number (optional - press Enter to skip): ") or None

    birth_date = input("Birth date(1999-2-14): ")

    print('-' * 10)
    try:
        user = User.register(username, password, birth_date, phone_number)

        if user:
            print(f"User created successfully.")
    except Exception as e:
        print(e)

def login_user():
    """Handles the user login process and returns the logged-in user object."""
    os.system('cls')
    print("---Login---")

    username = input("Username: ")
    password = getpass.getpass()

    logged_in_user = User.login(username, password)
    return logged_in_user

def edit_user_profile(logged_in_user):
    """Allows a logged-in user to edit their profile information."""
    os.system('cls')
    print("--- Update your Profile ---")

    print("if you dont want to change just press Enter")

    new_username = input("New Username: ") or None
    new_phone_number = input("New Phone number: ") or None
    new_birth_date = input("New Birthdate: ") or None

    if new_username:
        if logged_in_user.update_username(new_username):
            print("Username updated successfully.")
    if new_phone_number:
        if logged_in_user.update_phone_number(new_phone_number):
            print("Phone number updated successfully.")
    if new_birth_date:
        if logged_in_user.update_birth_date(new_birth_date):
            print("Birthdate updated successfully.")

def edit_user_password(logged_in_user):
    """Allows a logged-in user to change their password."""
    os.system('cls')
    print("--- Change Password ---")

    old_password = getpass.getpass("Old Password: ")
    new_password = getpass.getpass("New Password: ")
    confirm_password = getpass.getpass("Confirm New Password: ")

    logged_in_user.update_password(old_password, new_password, confirm_password)


def main():
    """
    Initializes and runs the main application loop.

    Displays the main menu and handles user navigation for creating a new user,
    logging in, or exiting the application. It also manages the sub-menu
    for logged-in users.
    """
    logged_in_user = None

    while True:
        print("--- Menu ---")
        print("  1.New User")
        print("  2.Login")
        print("  0.Exit")
        try:
            menu_number = int(input("Enter your choice number: "))

            if menu_number == 1:
                try:
                    register_user()
                except Exception as e:
                    print(e)
            elif menu_number == 2:
                try:
                    logged_in_user = login_user()
                except Exception as e:
                    print(e)

                if logged_in_user:
                    os.system('cls')
                    while True:
                        print("--- Profile ---")
                        print("  1.Show Information")
                        print("  2.Edit Profile")
                        print("  3.Change Password")
                        print("  4.Logout") #back to main menu

                        try:
                            profile_choice = int(input("Enter your choice number: "))

                            if profile_choice == 1:
                                os.system('cls')
                                print(logged_in_user)

                            elif profile_choice == 2:
                                try:
                                    edit_user_profile(logged_in_user)
                                except Exception as e:
                                    print(e)

                            elif profile_choice ==3:
                                try:
                                    edit_user_password(logged_in_user)
                                except Exception as e:
                                    print(e)

                            elif profile_choice ==4:
                                os.system('cls')
                                logged_in_user = None
                                break
                        except ValueError as e:
                            print("Invalid choice, please try again." , e)
                else:
                    os.system('cls')
                    print("Login failed. Please check your credentials.")

            elif menu_number == 0:
                os.system('cls')
                break
        except ValueError:

            print("Invalid choice, please try again.")




if __name__ == '__main__':
    main()