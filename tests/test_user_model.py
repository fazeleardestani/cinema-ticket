import unittest
import jdatetime

from exeptions import UsernameExistsError, InvalidCredentialsError, InsufficientFundsError
from models.cinema import Showing, Movies
from models.user import User


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.original_users = list(User.users)
        User.users = []

        self.original_showings = list(Showing.showings)
        Showing.showings = []

        self.test_user = User.register(
            username="testuser",
            password="password123",
            birth_date="1380-06-12"
        )

        self.test_user_bank = self.test_user.create_bank_account('1234')
        self.test_user_bank.balance = 100
        self.test_user.wallet_balance = 100

        movie = Movies("Inception", 17)

        self.test_showing = Showing.create_showing(movie,80 , 80,  "1404-06-15 22:00")
    def tearDown(self):
        User.users = self.original_users
        Showing.showings = self.original_showings



    def test_register_user(self):
        self.assertEqual(self.test_user.username, "testuser")
        self.assertEqual(len(User.users), 1)
    def test_register_fail_with_duplicate_username(self):
        with self.assertRaises(UsernameExistsError):
            User.register(
                username="testuser",
                password="password",
                birth_date="1390-01-01"
            )
        self.assertEqual(len(User.users), 1)

    def test_login_succeeds_with_correct_credentials(self):
        user = User.login("testuser", "password123")
        self.assertIsInstance(user, User)

    def test_login_fails_with_incorrect_password(self):
        with self.assertRaises(InvalidCredentialsError):
            User.login("testuser", "password")

    def test_login_fails_with_incorrect_username(self):
        with self.assertRaises(InvalidCredentialsError):
            User.login("test user", "password")

    def test_get_age_returns_correct_age(self):
        self.assertEqual(self.test_user.get_age() , 24)

    def test_get_membership_months_returns_correct_duration(self):
        self.assertEqual(self.test_user.get_membership_months() ,0)

    def test_charge_wallet_increases_balance(self):
        self.test_user.charge_wallet(50,
                                     self.test_user_bank,
                                     "1234",
                                     self.test_user_bank.cvv2)
        self.assertEqual(self.test_user.wallet_balance , 150)

    def test_book_ticket_succeeds_with_enough_balance(self):
        self.test_user.book_ticket(self.test_showing)
        self.assertEqual(len(self.test_showing.reserved_seat) ,1)

    def test_book_ticket_fails_with_insufficient_funds(self):
        self.test_user.wallet_balance = 10
        with self.assertRaises(InsufficientFundsError):
            self.test_user.book_ticket(self.test_showing)
        self.assertEqual(len(self.test_showing.reserved_seat), 0)

    def test_book_ticket_applies_birthday_discount(self):
        self.test_user.birth_date = "1381-06-15"
        self.test_user.book_ticket(self.test_showing)
        self.assertEqual(self.test_user.wallet_balance , 60)

    def test_book_ticket_applies_gold_cashback(self):
        self.test_user.subscription = 'gold'
        self.test_user.cashback_percent = 50
        self.test_user.cashback_date = jdatetime.datetime.now() + jdatetime.timedelta(days=5)

        self.test_user.book_ticket(self.test_showing)
        self.assertEqual(self.test_user.wallet_balance, 60)

    def test_book_ticket_applies_silver_cashback(self):
        self.test_user.subscription = 'silver'
        self.test_user.cashback_percent = 20
        self.test_user.cashback_count=3
        self.test_user.book_ticket(self.test_showing)
        self.assertEqual(self.test_user.wallet_balance, 36)








