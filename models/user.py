"""
This module defines the User class and its related management functions.

It includes functionalities for creating, validating, and managing user accounts
as part of the user management system.
"""
from __future__ import annotations
import inspect
from datetime import datetime
from uuid import uuid4
import hashlib
import re
from custom_log import logger as log
from exeptions import InvalidPasswordError, InvalidBirthDateError, UsernameExistsError, PasswordsDoesNotMatchError, \
    InvalidCredentialsError
from utils import data_load , data_dump

FILE_PATH = 'data/user.json'

def _hash_password(password: str) -> str:
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode('utf8')).hexdigest()

def unique_username(func):
    """Decorator to ensure the username is not already taken."""
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)

        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        username = bound_args.arguments.get('username') or bound_args.arguments.get('new_username')
        for user in User.users:
            if username == user['username']:
                log.warning( "User '{}' already exists.".format(username))
                raise UsernameExistsError
        return func(*args, **kwargs)
    return wrapper

class User:
    """A class to represent and manage users."""

    users = data_load(FILE_PATH) or []

    def __init__(self , username:str ,password:str, birth_date:str, phone_number:str = None)->None:
        """Initializes a new user instance."""
        self.uid = str(uuid4())
        self.username = username
        self.phone_number = phone_number
        self._password = _hash_password(password)
        self.birth_date = birth_date
        self.__created_at = datetime.now()
        self.is_hashed = True

    @staticmethod
    def _validate_password_length(password):
        """Validates if the password meets the minimum length requirement.
        Raises InvalidPasswordError if the length is insufficient."""
        if len(password) < 4:
            log.warning('Password must be at least 4 characters.')
            raise InvalidPasswordError
        return True

    @staticmethod
    def _validate_password_confirmation(new_password , confirm_password):
        """Validates if the new password matches its confirmation.
           Raises PasswordsDoesNotMatchError if they don't match."""
        if new_password != confirm_password:
            log.warning('New password and confirmation passwords do not match.')
            raise PasswordsDoesNotMatchError
        return True

    @staticmethod
    def _validate_birth_date(birth_date:str):
        print(birth_date)
        birth_date_pattern = r"\b\d{4}-(0?[1-9]|1[0-2])-(0?[1-9]|[12]\d|3[01])\b"
        if re.fullmatch(birth_date , birth_date_pattern):
            log.warning("Validation failed for birth date: '{}'. Format should be YYYY-M-D or YYYY-MM-DD.".format(birth_date))
            raise InvalidBirthDateError
        return True

    def to_dict(self):
        """turn user object to dictionary."""
        return {
            'uid': self.uid,
            'username': self.username,
            'phone_number': self.phone_number,
            'password': self._password,
            'birth_date': self.birth_date,
            'created_at': self.__created_at.isoformat(),
            'is_hashed': self.is_hashed
        }

    @classmethod
    def from_dict(cls, data:dict):
        """ creates a new user instance from a dictionary(user lists)"""
        user_instance = cls.__new__(cls)
        user_instance.uid = data['uid']
        user_instance.username = data['username']
        user_instance._password = data['password']
        user_instance.birth_date = data['birth_date']
        user_instance.phone_number = data['phone_number']
        user_instance.__created_at = datetime.fromisoformat(data['created_at'])
        user_instance.is_hashed = data['is_hashed']
        return user_instance

    @classmethod
    def update_user(cls, self_user):
        """ update user information in users list file."""
        for user in cls.users:
            if user['uid'] == self_user.uid:
                user['username'] = self_user.username
                user['password'] = self_user._password
                user['birth_date'] = self_user.birth_date
                user['phone_number'] = self_user.phone_number
        data_dump(FILE_PATH, cls.users)

    @classmethod
    @unique_username
    def register(cls , username:str , password:str , birth_date:str , phone_number:str = None) -> User:
        """ Registers a new user. """
        if cls._validate_password_length(password) and cls._validate_birth_date(birth_date):
            user = cls(username, password, birth_date, phone_number)
            cls.users.append(user.to_dict())
            data_dump(FILE_PATH, cls.users)
            return user

    @classmethod
    def login(cls , username:str , password:str) -> User | None:
        """ user login function. """
        found_user = None
        for user in cls.users:
            if user['username'] == username and user['password'] == _hash_password(password):
                found_user = cls.from_dict(data=user)
                return found_user

        log.warning('User {} not found.'.format(username))
        raise InvalidCredentialsError

    @unique_username
    def update_username(self, new_username: str) -> bool:
        """Allows a logged-in user to updates a user's username."""
        self.username = new_username
        self.update_user(self)


        return True

    def update_phone_number(self, new_phone_number: str) -> bool:
        """Allows a logged-in user to updates a user's phone number."""
        self.phone_number = new_phone_number
        self.update_user(self)
        return True

    def update_birth_date(self, new_birth_date: str) -> bool:
        """Allows a logged-in user to updates a user's birthdate."""
        if self._validate_birth_date(new_birth_date):
            self.birth_date = new_birth_date
            self.update_user(self)
            return True

    def update_password(self, old_password: str, new_password: str, confirm_password: str) -> bool | None:
        """updates a user's password."""
        if self._password != _hash_password(old_password):
            log.warning('Old password does not match.')
            raise PasswordsDoesNotMatchError

        self._validate_password_length(new_password)
        self._validate_password_confirmation(new_password, confirm_password)

        self._password = _hash_password(new_password)
        self.update_user(self)
        log.info('Password updated.')
        return True

    def __str__(self):
        """Returns a user-friendly string representation of the user."""
        return f'\nUser ID: {self.uid},\nUsername: {self.username},\nPhone Number: {self.phone_number}\nBirthDate: {self.birth_date}\n'














