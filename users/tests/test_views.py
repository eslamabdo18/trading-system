import json
from django.core.exceptions import SuspiciousOperation

from django.test import TestCase
from rest_framework import status
from datetime import date
from users.models import User
from stocks.models import Stock


class UsersViewsTestCase(TestCase):

    def create_stock(self) -> Stock:
        return Stock.objects.create(stock_id="469b77c8-290d-428b-8230-6cff7396e998", name="CIB",
                                    price=20, availability=120, timestamp=date.today())

    def setUp(self) -> None:
        # set up user object
        self.user = User.objects.create(
            username="test1", email="test@gmail.com", password="test1234", balance=2000)

        self.stock = self.create_stock()
        # set up urls
        self.list_users_url = '/api/users/'
        self.user_retrive_url = '/api/users/{id}/'

        self.deposit_url = '/api/users/{id}/deposit'
        self.withdraw_url = '/api/users/{id}/withdraw'
        self.sell_url = '/api/users/{id}/sell'
        self.buy_url = '/api/users/{id}/buy'

    def test_list_all_users(self):
        res = self.client.get(self.list_users_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_get_user_success(self):
        res = self.client.get(self.user_retrive_url.format(id=self.user.id))
        self.assertEquals(res.status_code, status.HTTP_200_OK)

        self.assertEquals(res.data['balance'], self.user.balance)
        self.assertEquals(res.data['email'], self.user.email)
        self.assertEquals(res.data['username'], self.user.username)

    def test_get_user_fail(self):
        res = self.client.get(self.user_retrive_url.format(id=50000))
        self.assertEquals(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_with_no_stocks(self):
        res = self.client.get(self.user_retrive_url.format(id=self.user.id))
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data["stocks"]), 0)

    def test_deposit_success(self):
        data = {
            "amount": 100,
        }
        res = self.client.post(
            self.deposit_url.format(id=self.user.id), data=data)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data["balance"], self.user.balance+100)

    def test_deposit_no_body_fail(self):

        res = self.client.post(self.deposit_url.format(id=self.user.id))
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(res.data)
        self.assertIn('amount', res.data)
        self.assertIn('This field is required.', res.data["amount"])

    def test_deposit_invalid_user_id(self):
        data = {
            "amount": 100,
        }
        res = self.client.post(self.deposit_url.format(id=50505), data=data)
        self.assertEquals(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_withdraw_success(self):
        data = {
            "amount": 100,
        }
        res = self.client.post(
            self.withdraw_url.format(id=self.user.id), data=data)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data["balance"], self.user.balance-100)

    def test_withdraw_no_body_fail(self):

        res = self.client.post(self.withdraw_url.format(id=self.user.id))
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(res.data)
        self.assertIn('amount', res.data)
        self.assertIn('This field is required.', res.data["amount"])

    def test_withdraw_no_enough_balance(self):
        data = {
            "amount": 4000,
        }
        res = self.client.post(
            self.withdraw_url.format(id=self.user.id), data=data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(res.data["error"],
                          "you dont have the fund to withdraw")

    def test_withdraw_invalid_user_id(self):
        data = {
            "amount": 100,
        }
        res = self.client.post(self.withdraw_url.format(id=50505), data=data)
        self.assertEquals(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_buy_success(self):
        data = {
            "stock_id": "469b77c8-290d-428b-8230-6cff7396e998",
            "total": 10,
            "lower_bound": 1,
            "upper_bound": 40
        }
        res = self.client.post(
            self.buy_url.format(id=self.user.id), data=data)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        # self.assertEquals(res.data['messages'], "your order is being placed")

    def test_buy_more_than_balance_fail(self):
        data = {
            "stock_id": "469b77c8-290d-428b-8230-6cff7396e998",
            "total": 500,
            "lower_bound": 1,
            "upper_bound": 500
        }
        res = self.client.post(
            self.buy_url.format(id=self.user.id), data=data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(res, SuspiciousOperation)
