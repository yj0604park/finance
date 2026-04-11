from django.test import TestCase

from money.models.accounts import Account, Bank


class AccountBankTest(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(name="Test Bank")
        Account.objects.create(name="lion", bank=self.bank, amount=1000)
        Account.objects.create(name="cat", bank=self.bank, amount=500)

    def test_account(self):
        """Account are correctly identified"""
        lion = Account.objects.get(name="lion")
        cat = Account.objects.get(name="cat")
        self.assertIsNotNone(lion)
        self.assertIsNotNone(cat)
        self.assertEqual(lion.bank.name, "Test Bank")
        self.assertEqual(cat.bank.name, "Test Bank")
