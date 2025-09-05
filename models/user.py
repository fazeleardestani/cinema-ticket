"""
This module defines the User class and its related management functions.

It includes functionalities for creating, validating, and managing user accounts
as part of the user management system.
"""
from __future__ import annotations

from enum import Enum
from uuid import uuid4
import inspect
import jdatetime

from custom_log import logger as log
from models.bank import BankAccount as Bank
from exeptions import InvalidPasswordError, InvalidDateError, UsernameExistsError, PasswordsDoesNotMatchError, \
    InvalidCredentialsError, InvalidAccountNumberError, InvalidChoiceError, InsufficientFundsError
from models.cinema import Showing
from utils import data_load, data_dump, hash_password, str_to_datetime, calculate_time_span, apply_discount, \
    str_to_showimg_datetime

FILE_PATH = 'data/user.json'
SUBSCRIPTION_DICT = {
    'bronze': 0,
    'silver': 20,
    'gold': 30,
}

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

class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'

class User:
    """A class to represent and manage users."""

    users = data_load(FILE_PATH) or []

    def __init__(self , username:str ,password:str, birth_date:str, phone_number:str = None, role = UserRole.USER)->None:
        """Initializes a new user instance."""
        self.role = role
        self.uid = str(uuid4())
        self.username = username
        self.phone_number = phone_number
        self._password = hash_password(password)
        self.birth_date = birth_date
        self.bank_accounts = []
        self.wallet_balance = 0
        self.subscription = 'bronze'
        self.cashback_count = 0
        self.cashback_date = jdatetime.datetime.now()
        self.cashback_percent = 0
        self.gift = None
        self.__created_at = jdatetime.datetime.now()
        self.is_hashed = True

    @staticmethod
    def _validate_password_length(password:str):
        """Validates if the password meets the minimum length requirement.
        Raises InvalidPasswordError if the length is insufficient."""
        if len(password) < 4:
            log.warning('Password must be at least 4 characters.')
            raise InvalidPasswordError
        return True

    @staticmethod
    def _validate_password_confirmation(new_password:str , confirm_password:str):
        """Validates if the new password matches its confirmation.
           Raises PasswordsDoesNotMatchError if they don't match."""
        if new_password != confirm_password:
            log.warning('New password and confirmation passwords do not match.')
            raise PasswordsDoesNotMatchError
        return True

    def get_age(self)->int:
        birth_date = str_to_datetime(self.birth_date)
        now = jdatetime.datetime.now()
        age = calculate_time_span(birth_date , now).days // 365
        return int(age)

    def get_remaining_subscription_days(self)->int:
        if self.subscription != 'gold':
            return 0
        now = jdatetime.datetime.now()

        if self.cashback_date > now:
            time_span = calculate_time_span(now , self.cashback_date)
            return time_span.days
        else:
            return 0

    def get_membership_months(self)->int:

        now = jdatetime.datetime.now()

        time_span = calculate_time_span(self.__created_at , now)
        return int(time_span.days // 30)

    def to_dict(self):
        """turn user object to dictionary."""
        return {
            'role': self.role.value,
            'uid': self.uid,
            'username': self.username,
            'phone_number': self.phone_number,
            'password': self._password,
            'birth_date': self.birth_date,
            'bank_accounts' : self.bank_accounts,
            'wallet_balance': self.wallet_balance,
            'subscription' : self.subscription,
            'cashback_count' : self.cashback_count,
            'cashback_date' : self.cashback_date.isoformat(),
            'cashback_percent' : self.cashback_percent,
            'gift' : self.gift,
            'created_at': self.__created_at.isoformat(),
            'is_hashed': self.is_hashed
        }

    @classmethod
    def from_dict(cls , user_dict:dict):
        """ creates a new user instance from a dictionary(user lists)"""
        user_instance = cls.__new__(cls)
        user_instance.role = UserRole(user_dict['role'])
        user_instance.uid = user_dict['uid']
        user_instance.username = user_dict['username']
        user_instance._password = user_dict['password']
        user_instance.birth_date = user_dict['birth_date']
        user_instance.phone_number = user_dict['phone_number']
        user_instance.bank_accounts = [Bank.from_dict(account) for account in user_dict['bank_accounts']]
        user_instance.wallet_balance = user_dict['wallet_balance']
        user_instance.subscription = user_dict['subscription']
        user_instance.cashback_count = user_dict['cashback_count']
        user_instance.cashback_percent = user_dict['cashback_percent']
        user_instance.gift = user_dict['gift']
        user_instance.is_hashed = user_dict['is_hashed']

        iso_format = "%Y-%m-%dT%H:%M:%S.%f"
        user_instance.cashback_date = jdatetime.datetime.strptime(user_dict['cashback_date'], iso_format)
        user_instance.__created_at = jdatetime.datetime.strptime(user_dict['created_at'] , iso_format)

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
                user['bank_accounts'] = [account.to_dict() for account in self_user.bank_accounts]
                user['wallet_balance'] = self_user.wallet_balance
                user['subscription'] = self_user.subscription
                user['cashback_count'] = self_user.cashback_count
                user['cashback_date'] = self_user.cashback_date.isoformat()
                user['cashback_percent'] = self_user.cashback_percent
                user['gift'] = self_user.gift

        data_dump(FILE_PATH, cls.users)

    @classmethod
    @unique_username
    def register(cls , username:str , password:str , birth_date:str , phone_number:str = None) -> User:
        """ Registers a new user. """
        if cls._validate_password_length(password) and str_to_datetime(birth_date):
            user = cls(username, password, birth_date, phone_number)
            cls.users.append(user.to_dict())
            data_dump(FILE_PATH, cls.users)
            return user

    @classmethod
    def login(cls , username:str , password:str) -> User | None:
        """ user login function. """
        found_user = None
        for user in cls.users:
            if user['username'] == username and user['password'] == hash_password(password):
                found_user = cls.from_dict(user)
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
        if str_to_datetime(new_birth_date):
            self.birth_date = new_birth_date
            self.update_user(self)
            return True

    def update_password(self, old_password: str, new_password: str, confirm_password: str) -> bool | None:
        """updates a user's password."""
        if self._password != hash_password(old_password):
            log.warning('Old password does not match.')
            raise PasswordsDoesNotMatchError

        self._validate_password_length(new_password)
        self._validate_password_confirmation(new_password, confirm_password)

        self._password = hash_password(new_password)
        self.update_user(self)
        log.info('Password updated.')
        return True

    def create_bank_account(self , bank_account_password:str):
        """Creates a new bank account for the user."""
        bank_account = Bank.create_account(self.uid, bank_account_password)
        self.bank_accounts.append(bank_account)
        self.update_user(self)
        return bank_account

    def charge_wallet(self , amount:int , bank_account , account_password:str , account_cvv2:int):
        """Charges the user's wallet by withdrawing from a bank account."""
        bank_account.withdraw(amount , account_password , account_cvv2)
        self.wallet_balance += amount
        self.update_user(self)

    def deposit_to_bank_account(self , account_number:str , amount:int):
        """Deposits a specified amount into one of the user's bank accounts."""
        for bank_account in self.bank_accounts:
            if bank_account.account_number == account_number:
                return bank_account.deposit(amount)

    def withdraw_from_bank_account(self , account_number:str , account_password:str , account_cvv2:str ,  amount:int):
        """Withdraws a specified amount from one of the user's bank accounts."""
        for bank_account in self.bank_accounts:
            if bank_account.account_number == account_number:
                return bank_account.withdraw(amount , account_password , account_cvv2)

    def change_subscription(self , subscription_number:str):
        """Changes the user's subscription plan."""

        if subscription_number == "1":
            subscription_type = "silver"
        elif subscription_number == "2":
            subscription_type = "gold"
        else:
            log.warning('Invalid Subscription Number. Please enter number of your subscription')
            raise InvalidChoiceError
        if self.wallet_balance >= SUBSCRIPTION_DICT[subscription_type]:

            self.wallet_balance -= SUBSCRIPTION_DICT[subscription_type]
            self.subscription = subscription_type
            if subscription_type == 'silver':
                self.cashback_count = 3
                self.cashback_percent = 20

            if subscription_type == 'gold':
                self.cashback_date = jdatetime.datetime.now() + jdatetime.timedelta(days=30)
                self.cashback_percent = 50
                self.gift = 'a free Soda'

            self.update_user(self)
            return True

        else:
            log.warning(f'User {self.username} has insufficient funds to buy {subscription_type} subscription.')
            raise InsufficientFundsError

    def book_ticket(self , showing:Showing):
        """Handles the entire ticket booking process for a user."""
        birth_date_obj = str_to_datetime(self.birth_date)
        showing_time_obj = str_to_showimg_datetime(showing.showing_time)
        now_obj = jdatetime.datetime.now()

        # ۲. بررسی شرط تولد به صورت صحیح و خوانا
        is_birthday_on_showing_date = (birth_date_obj.month == showing_time_obj.month and
                                       birth_date_obj.day == showing_time_obj.day)

        is_birthday_on_reserve_date = (birth_date_obj.month == now_obj.month and
                                       birth_date_obj.day == now_obj.day)

        birth_date_check = is_birthday_on_showing_date or is_birthday_on_reserve_date

        membership_months = self.get_membership_months()

        birth_day_discount = 0
        if birth_date_check:
            birth_day_discount = 50

        final_price = apply_discount(showing.price, membership_months + birth_day_discount)

        if final_price > self.wallet_balance:
            log.warning(f'User {self.username} has insufficient funds to buy {showing.movie_name} ticket.')
            raise InsufficientFundsError

        self.wallet_balance -= final_price
        showing.reserved_seat.append(self.uid)

        percent = lambda x : x/100
        if self.subscription == 'silver' and self.cashback_count != 0:
            self.wallet_balance += final_price * percent(self.cashback_percent)
            self.cashback_count -=1
            log.info(
                     f"{self.cashback_percent}% of your purchase has been returned to your wallet as cashback.")
            if self.cashback_count == 0:
                self.subscription = 'bronze'
        if self.subscription == 'gold' and self.cashback_date != jdatetime.datetime.now():
            self.wallet_balance += final_price * percent(self.cashback_percent)
            log.info(
                     f"{self.cashback_percent}% of your purchase has been returned to your wallet as cashback, along with {self.gift} for the movie.")

        self.update_user(self)
        Showing.update_show(showing)

    def __str__(self):
        """Returns a user-friendly string representation of the user."""
        return f'\nUser ID: {self.uid},\nUsername: {self.username},\nPhone Number: {self.phone_number}\nBirthDate: {self.birth_date}\n'














