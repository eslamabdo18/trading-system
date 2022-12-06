from django.test import TestCase
from users.models import User, UserTransaction
from stocks.models import Stock
from django.utils import timezone
from datetime import date

# models test


class UsersModelsTest(TestCase):

    def create_user(self, username="test1", email="test@gmail.com", password="test1234"):
        return User.objects.create(username=username, email=email, password=password)

    def create_stock(self):
        return Stock.objects.create(stock_id="id-50", name="CIB",
                                    price=20, availability=120, timestamp=date.today())

    def create_user_transaction(self, type=1):
        user = self.create_user()
        stock = self.create_stock()
        # print(stock)
        return UserTransaction.objects.create(
            user=user, stock=stock, total_price=500, total_count=10, type=type)

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, "test1")

    def test_user_balance(self):
        # user balance should be 0 by default
        user = self.create_user()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.balance, 0)

    def test_user_change_balance(self):
        # user balance should be 0 by default
        user = self.create_user()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.balance, 0)

        user.balance = 500
        self.assertEqual(user.balance, 500)

    def test_buy_user_transaction_creation(self):
        transaction = self.create_user_transaction()
        self.assertTrue(isinstance(transaction, UserTransaction))
        self.assertEqual(transaction.type, 1)
        self.assertEqual(transaction.total_price, 500)

    def test_sell_user_transaction_creation(self):
        transaction = self.create_user_transaction(type=2)
        self.assertTrue(isinstance(transaction, UserTransaction))
        self.assertEqual(transaction.type, 2)
        self.assertEqual(transaction.total_price, 500)
