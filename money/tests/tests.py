# Create your tests here.
from django.test import TestCase

from .models import Account, Bank


class AnimalTestCase(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(name="Test Bank")
        Account.objects.create(name="lion", bank=self.bank)
        Account.objects.create(name="cat", bank=self.bank)

    def test_account(self):
        """Account are correctly identified"""
        lion = Account.objects.get(name="lion")
        cat = Account.objects.get(name="cat")
        self.assertNotEqual(lion, None)
        self.assertNotEqual(cat, None)
        self.assertEqual(lion.bank.name, "Test Bank")
        self.assertEqual(cat.bank.name, "Test Bank")
