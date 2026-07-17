import sys
sys.path.insert(0, '.')
from database import DatabaseManager
from customer import create_customer

db = DatabaseManager(use_sqlite=True)
db.init_db()
db.seed_default_admin()
print(create_customer(db, 'Alice', 'alice@example.com', '123', 'Addr', 'Savings', 1000))
db.close()
