import random
from custom_log import logger as log
from exeptions import InvalidPasswordError, InvalidCvv2Error, NegativeAmountError, InvalidAccountNumberError, \
    NotEnoughAmountError
from utils import data_load , data_dump , hash_password

FILE_PATH = 'data/bank.json'


def unique_account_number(account_list: list) -> str:
    """Generates a unique 8-digit account number."""
    existing_numbers = {account['account_number'] for account in account_list}
    while True:
        account_number = str(random.randint(10_000_000, 99_999_999))

        if account_number not in existing_numbers:
            return account_number


class BankAccount:
    """A class to manage bank accounts, including creation and transactions."""

    accounts = data_load(FILE_PATH) or []

    def __init__(self, owner_uid: str, password: str, account_number: str):
        """Initializes a new bank account instance."""
        self.owner_uid = owner_uid
        self.__account_number = account_number
        self.password = hash_password(password)
        self.cvv2 = random.randint(100, 9_999)
        self.balance = 0

    def __str__(self):
        """Returns a user-friendly string representation of the bank account."""
        return f"Account Number: {self.__account_number} , Account Cvv2: {self.cvv2}"

    @staticmethod
    def _validate_password_length(password:str):
        """Validates if the password meets standard length requirement.
        Raises InvalidPasswordError if the length is insufficient."""
        if len(password) != 4:
            log.warning('Password must be 4 characters.')
            raise InvalidPasswordError
        return True

    def _security_check(self , password:str , cvv2:int):
        """Verifies the transaction password and CVV2."""
        if self.password != hash_password(password):
            log.warning('Password is incorrect.')
            raise InvalidPasswordError
        elif self.cvv2 != cvv2:
            log.warning('CVV2 is incorrect.')
            raise InvalidCvv2Error
        else:
            return True

    def to_dict(self) -> dict:
        """Converts the bank account object to a dictionary."""
        return {
            'owner_uid': self.owner_uid,
            'account_number': self.__account_number,
            'password': self.password,
            'cvv2': self.cvv2,
            'balance': self.balance,
        }

    @classmethod
    def from_dict(cls, account_dict:dict):
        """Creates a new bank account instance from a dictionary."""
        account_instance = cls.__new__(cls)
        account_instance.owner_uid = account_dict['owner_uid']
        account_instance.__account_number = account_dict['account_number']
        account_instance.password = account_dict['password']
        account_instance.cvv2 = account_dict['cvv2']
        account_instance.balance = account_dict['balance']
        return account_instance

    @classmethod
    def update_account(cls, self_account):
        """Updates a bank account's information in the accounts list file."""
        for account in cls.accounts:
            if account['account_number'] == self_account.__account_number:
                account['balance'] = self_account.balance

        data_dump(FILE_PATH, cls.accounts)

    @classmethod
    def create_account(cls, owner_uid: str, password: str):
        """Creates a new bank account, saves it, and returns the instance."""
        if cls._validate_password_length(password):
            account_number = unique_account_number(cls.accounts)
            account = cls(owner_uid, password, account_number)
            cls.accounts.append(account.to_dict())
            data_dump(FILE_PATH, cls.accounts)
            return account


    def deposit(self,  amount:int):
        """Deposits a specified amount into the account."""
        if amount <= 0:
            log.warning('Amount must be positive.')
            raise NegativeAmountError
        self.balance += amount
        self.update_account(self)
        log.info('balance updated')


    def withdraw(self, amount:int , password:str , cvv2:int):
        """Withdraws a specified amount after verifying credentials."""
        if self._security_check(password, cvv2):
            min_check = self.balance - amount
            if self.balance >= amount and min_check > 10:
                self.balance -= amount
                self.update_account(self)
                log.info('balance updated')
            else:
                log.info('account balance is insufficient.')
                raise NotEnoughAmountError


    def transfer(self):
        """Transfers funds from this account to another."""
        pass











