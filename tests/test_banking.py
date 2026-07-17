import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import DatabaseManager
from customer import create_customer, get_customer_details, update_customer, delete_customer
from deposit import deposit_money
from withdraw import withdraw_money
from transfer import transfer_money
from statement import get_statement


class BankingSystemTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, "banking.sqlite3")
        self.db = DatabaseManager(db_path=self.db_path)
        self.db.init_db()
        self.db.seed_default_admin()

    def tearDown(self):
        self.db.close()
        self.tmp_dir.cleanup()

    def test_database_initialization_creates_tables(self):
        tables = self.db.list_tables()
        self.assertIn("customers", tables)
        self.assertIn("login", tables)
        self.assertIn("transactions", tables)
        self.assertIn("transfers", tables)

    def test_customer_lifecycle(self):
        account_no = create_customer(
            db=self.db,
            name="Alice",
            email="alice@example.com",
            phone="1234567890",
            address="123 Main St",
            account_type="Savings",
            initial_balance=1000.00,
        )
        self.assertTrue(account_no > 0)

        customer = get_customer_details(self.db, account_no)
        self.assertEqual(customer["name"], "Alice")
        self.assertEqual(float(customer["balance"]), 1000.00)

        update_customer(self.db, account_no, name="Alice Updated", email="alice.updated@example.com")
        updated = get_customer_details(self.db, account_no)
        self.assertEqual(updated["name"], "Alice Updated")

        delete_customer(self.db, account_no)
        self.assertIsNone(get_customer_details(self.db, account_no))

    def test_account_number_and_ifsc_are_generated(self):
        account_no = create_customer(
            db=self.db,
            name="Dana",
            email="dana@example.com",
            phone="5555555555",
            address="456 Side St",
            account_type="Savings",
            initial_balance=250.00,
        )
        customer = get_customer_details(self.db, account_no)
        self.assertGreater(account_no, 0)
        self.assertEqual(customer["ifsc_code"], "BKID0001001")

    def test_deposit_withdraw_and_transfer(self):
        sender = create_customer(self.db, "Bob", "bob@example.com", "1111111111", "London", "Current", 500.00)
        receiver = create_customer(self.db, "Cara", "cara@example.com", "2222222222", "Paris", "Savings", 300.00)

        deposit_money(self.db, sender, 200.00)
        withdraw_money(self.db, sender, 100.00)
        transfer_money(self.db, sender, receiver, 50.00)

        sender_details = get_customer_details(self.db, sender)
        receiver_details = get_customer_details(self.db, receiver)
        self.assertEqual(float(sender_details["balance"]), 550.00)
        self.assertEqual(float(receiver_details["balance"]), 350.00)

        statements = get_statement(self.db, sender)
        self.assertGreaterEqual(len(statements), 3)


if __name__ == "__main__":
    unittest.main()
