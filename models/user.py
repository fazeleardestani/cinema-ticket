"""
This module defines the User class.

It includes functionalities for creating, validating, and managing user accounts
as part of the user management system.
"""
from __future__ import annotations
from uuid import uuid4
from datetime import datetime
import hashlib
import inspect


def _hash_password(password: str) -> str:
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode('utf8')).hexdigest()


def unique_username(func):
    """Decorator to ensure the username is not already taken."""
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)

        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        username = bound_args.arguments.get(
            'username') or bound_args.arguments.get('new_username')
        for user in User.users.values():
            if username == user.username:
                print(f"User {username} already exists.")
                return
        return func(*args, **kwargs)
    return wrapper


class User:
    """A class to represent and manage users."""
    users = {}

    def __init__(self, username: str, password: str, birth_date: str, phone_number: str = None) -> None:
        """Initializes a new user instance."""
        self.uid = uuid4()
        self.username = username
        self.phone_number = phone_number
        self._password = _hash_password(password)
        self.birth_date = birth_date
        self.__created_at = datetime.now()

    @staticmethod
    def _validate_password_length(password: str) -> bool:
        """Static method to validate ONLY the password's length."""
        if len(password) < 4:
            print("Password must be at least 4 characters.")
            return False
        return True

    @staticmethod
    def _validate_password_confirmation(password: str, confirm_password: str) -> bool:
        """Static method to validate ONLY the password's confirmation."""
        if password != confirm_password:
            print("\nPasswords do not match.")
            return False
        return True

    @classmethod
    @unique_username
    def create_account(cls, username: str, password: str, birth_date: str, phone_number: str = None) -> User | None:
        """Creates, validates, and stores a new user account."""
        if not cls._validate_password_length(password):
            return
        user = cls(username, password, birth_date, phone_number)
        cls.users[user.uid] = user
        return user

    @classmethod
    def login(cls, username: str, password: str) -> User | None:
        """Handles the user login process."""
        found_user = None
        for user in cls.users.values():
            if user.username == username:
                found_user = user
                break

        if found_user:
            if found_user._password == _hash_password(password):
                return found_user
            else:
                return
        else:
            return

    @unique_username
    def update_username(self, new_username: str) -> bool:
        """Allows a logged-in user to updates a user's username."""
        self.username = new_username
        return True

    def update_phone_number(self, new_phone_number: str) -> bool:
        """Allows a logged-in user to updates a user's phone number."""
        self.phone_number = new_phone_number
        return True

    def update_password(self, old_password: str, new_password: str, confirm_password: str) -> bool | None:
        """updates a user's password."""
        if self._password != _hash_password(old_password):
            print("your old password do not match.")
            return
        if not User._validate_password_length(new_password):
            return
        if not self._validate_password_confirmation(new_password, confirm_password):
            return

        self._password = _hash_password(new_password)
        print('Password updated.')
        return True

    def __str__(self):
        """Returns a user-friendly string representation of the user."""
        return f'\nuser id: {self.uid},\nusername: {self.username},\nphone number: {self.phone_number}\n'
