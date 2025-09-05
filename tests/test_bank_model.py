import unittest

from exeptions import NegativeAmountError, InsufficientFundsError, NotEnoughAmountError, InvalidPasswordError, \
    InvalidAccountNumberError
from models.bank import BankAccount


class TestBankModel(unittest.TestCase):
    def setUp(self):
        self.original_bank_accounts = BankAccount.accounts
        BankAccount.accounts = []

        self.test_bank_account = BankAccount.create_account('owner uid',
                                                            '1234', )

        self.test_bank_account.balance = 50

    def tearDown(self):
        BankAccount.accounts = self.original_bank_accounts

    def test_create_account_succeeds(self):
        self.assertEqual(self.test_bank_account.owner_uid, 'owner uid')
        self.assertEqual(len(BankAccount.accounts), 1)

    def test_deposit_increases_balance(self):
        self.test_bank_account.deposit(100)
        self.assertEqual(self.test_bank_account.balance, 150)

    def test_deposit_fails_with_negative_amount(self):
        with self.assertRaises(NegativeAmountError):
            self.test_bank_account.deposit(-100)

    def test_withdraw_succeeds_with_correct_credentials(self):
        cvv2 = self.test_bank_account.cvv2
        self.test_bank_account.withdraw(10, '1234', cvv2)

        self.assertEqual(self.test_bank_account.balance, 40)

    def test_withdraw_fails_with_insufficient_balance(self):
        cvv2 = self.test_bank_account.cvv2

        with self.assertRaises(NotEnoughAmountError):
            self.test_bank_account.withdraw(45, '1234', cvv2)

        self.assertEqual(self.test_bank_account.balance, 50)

    def test_withdraw_fails_with_incorrect_password(self):
        cvv2 = self.test_bank_account.cvv2

        with self.assertRaises(InvalidPasswordError):
            self.test_bank_account.withdraw(45, '1212', cvv2)

        self.assertEqual(self.test_bank_account.balance, 50)

    def test_transfer_succeeds_with_valid_data(self):
        cvv2 = self.test_bank_account.cvv2
        destination_account = BankAccount.create_account('owner uid2',
                                                         '1234', )

        self.test_bank_account.transfer(20, '1234', cvv2,
                                        destination_account.account_number)
        self.assertEqual(self.test_bank_account.balance, 30)

    def test_transfer_fails_if_destination_not_found(self):
        cvv2 = self.test_bank_account.cvv2
        with self.assertRaises(InvalidAccountNumberError):
            self.test_bank_account.transfer(20, '1234', cvv2, '12345678')
        self.assertEqual(self.test_bank_account.balance, 50)
