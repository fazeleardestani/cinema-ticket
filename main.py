"""
This module serves as the main entry point for the user management application.

It handles the main menu, user interactions, and orchestrates calls
to the User class for registration, login, and profile management.
"""

import os
import getpass
from models.user import User

def register_user()->None:
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

def login_user()->User:
    """Handles the user login process and returns the logged-in user object."""
    os.system('cls')
    print("---Login---")

    username = input("Username: ")
    password = getpass.getpass()

    logged_in_user = User.login(username, password)
    return logged_in_user

def edit_user_profile(logged_in_user:User)->None:
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

def edit_user_password(logged_in_user:User)->None:
    """Allows a logged-in user to change their password."""
    os.system('cls')
    print("--- Change Password ---")

    old_password = getpass.getpass("Old Password: ")
    new_password = getpass.getpass("New Password: ")
    confirm_password = getpass.getpass("Confirm New Password: ")

    logged_in_user.update_password(old_password, new_password, confirm_password)

def charge_wallet(logged_in_user:User)->None:
    """Handles charging the user's wallet from a bank account."""
    os.system('cls')
    print("--- Charge Wallet ---")

    amount = int(input("Amount: "))

    if not logged_in_user.bank_accounts:
        print(" You don't have any bank accounts.")
        return

    print("Your Bank Accounts:")
    for i,bank_account in enumerate(logged_in_user.bank_accounts):
        print(f'{i+1}- {bank_account}')

    choice_str = input("Choose your account by number: ")
    choice_index = int(choice_str)-1

    bank_account =  logged_in_user.bank_accounts[choice_index]
    password = getpass.getpass("Bank Password: ")
    cvv2 = int(input("CVV2: "))

    logged_in_user.charge_wallet(amount , bank_account , password, cvv2)

def buy_subscription(logged_in_user:User)->None:
    """Handles the subscription purchase process."""
    os.system('cls')
    print("--- Buy Subscription ---")

    print(f"Your current wallet balance: {logged_in_user.wallet_balance}\n")

    print("\t1- Silver (20 coin): 3 times 20% cashback | price:20")
    print("\t2- Gold (30 coin): one month 50% cashback + one free soda | price: 30")
    subscription_number = input("\tChoose subscription number (1 or 2): ")

    if logged_in_user.change_subscription(subscription_number):
        print("Subscription changed successfully.")
        print(f"Your current wallet balance: {logged_in_user.wallet_balance}\n")

def main_create_bank_account(logged_in_user:User)->None:
    """Handles the creation of a new bank account for the user."""
    os.system('cls')
    print("--- Create Bank Account ---")
    account_password = input("Bank Account Password: ")
    bank_account = logged_in_user.create_bank_account(account_password)
    print("Account created successfully.")
    print(bank_account)

def main_deposit_bank_account(logged_in_user:User)->None:
    """Handles the depositing of a bank account for the user."""
    os.system('cls')
    print("--- Deposit Bank Account ---")

    if not logged_in_user.bank_accounts:
        print(" You don't have any bank accounts.")
        return

    print("Your Bank Accounts:")
    for i, bank_account in enumerate(logged_in_user.bank_accounts):
        print(f'{i + 1}- {bank_account}')

    choice_str = input("Choose your account by number: ")
    choice_index = int(choice_str) - 1

    bank_account = logged_in_user.bank_accounts[choice_index]
    amount = int(input("Amount: "))
    bank_account.deposit(amount)
    print("Bank account deposited successfully.")





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
                        print("  4.Create BankAccount")
                        print("  5.Deposit BankAccount")
                        print("  6.Charge Wallet")
                        print("  7.Buy Subscription")
                        print("  0.Logout") #back to main menu

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
                                try:
                                    main_create_bank_account(logged_in_user)
                                except Exception as e:
                                    print(e)

                            elif profile_choice ==5:
                                try:
                                    main_deposit_bank_account(logged_in_user)
                                except ValueError:
                                    print("Invalid amount or choice. Please enter numbers only.")
                                except Exception as e:
                                    print(e)

                            elif profile_choice ==6:
                                try:
                                    charge_wallet(logged_in_user)

                                except ValueError:
                                    print("Invalid amount or choice. Please enter numbers only.")
                                except Exception as e:
                                    print(e)

                            elif profile_choice ==7:
                                try:
                                    buy_subscription(logged_in_user)
                                except Exception as e:
                                    print(e)

                            elif profile_choice ==0:
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