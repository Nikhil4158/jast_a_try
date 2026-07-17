import os
import sqlite3
from typing import Optional

DEFAULT_IFSC_CODE = "BKID0001001"

try:
    import mysql.connector as mysql_connector
except ImportError:  # pragma: no cover - optional dependency
    mysql_connector = None


class DatabaseManager:
    def __init__(
        self,
        host: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        db_path: Optional[str] = None,
        use_sqlite: bool = False,
    ):
        self.use_sqlite = use_sqlite or os.getenv("BANK_DB_BACKEND", "sqlite").lower() == "sqlite"
        if self.use_sqlite:
            self.db_path = db_path or os.path.join(os.getcwd(), "banking.db")
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self._cursor = None
            return

        if mysql_connector is None:
            raise RuntimeError("mysql-connector-python is required for MySQL mode")

        try:
            self.connection = mysql_connector.connect(
                host=host or os.getenv("DB_HOST", "localhost"),
                user=user or os.getenv("DB_USER", "root"),
                ****** or os.getenv("DB_PASSWORD", ""),
                database=database or os.getenv("DB_NAME", "bank_db"),
                autocommit=False,
            )
        except Exception:
            self.use_sqlite = True
            self.db_path = db_path or os.path.join(os.getcwd(), "banking.db")
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        self._cursor = None

    def execute(self, query: str, params=()):
        if self.use_sqlite:
            sqlite_query = query.replace("%s", "?")
            cursor = self.connection.execute(sqlite_query, params)
            self._cursor = cursor
            return cursor

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params)
        self._cursor = cursor
        return cursor

    def fetchone(self):
        if self._cursor is None:
            return None
        return self._cursor.fetchone()

    def fetchall(self):
        if self._cursor is None:
            return []
        return self._cursor.fetchall()

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

    def init_db(self) -> None:
        if self.use_sqlite:
            self.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_no INTEGER UNIQUE,
                    ifsc_code TEXT NOT NULL DEFAULT 'BKID0001001',
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    address TEXT NOT NULL,
                    account_type TEXT NOT NULL,
                    balance REAL NOT NULL DEFAULT 0.0
                )
                """
            )
            columns = self.execute("PRAGMA table_info(customers)").fetchall()
            if not any(column[1] == "ifsc_code" for column in columns):
                self.execute("ALTER TABLE customers ADD COLUMN ifsc_code TEXT NOT NULL DEFAULT 'BKID0001001'")
            self.execute(
                """
                CREATE TABLE IF NOT EXISTS login (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
                """
            )
            self.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_no INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    balance_after REAL NOT NULL,
                    transaction_date TEXT NOT NULL
                )
                """
            )
            self.execute(
                """
                CREATE TABLE IF NOT EXISTS transfers (
                    transfer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_account INTEGER NOT NULL,
                    receiver_account INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    transfer_date TEXT NOT NULL
                )
                """
            )
            self.commit()
            return

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                account_no BIGINT UNIQUE,
                ifsc_code VARCHAR(15) NOT NULL DEFAULT 'BKID0001001',
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                address TEXT NOT NULL,
                account_type VARCHAR(20) NOT NULL,
                balance DECIMAL(10,2) NOT NULL DEFAULT 0.00
            )
            """
        )
        columns = self.execute("SHOW COLUMNS FROM customers").fetchall()
        if not any(column["Field"] == "ifsc_code" for column in columns):
            self.execute("ALTER TABLE customers ADD COLUMN ifsc_code VARCHAR(15) NOT NULL DEFAULT 'BKID0001001'")
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS login (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                role VARCHAR(20) NOT NULL
            )
            """
        )
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                account_no BIGINT NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                balance_after DECIMAL(10,2) NOT NULL,
                transaction_date DATETIME NOT NULL
            )
            """
        )
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS transfers (
                transfer_id INT AUTO_INCREMENT PRIMARY KEY,
                sender_account BIGINT NOT NULL,
                receiver_account BIGINT NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                transfer_date DATETIME NOT NULL
            )
            """
        )
        self.commit()

    def seed_default_admin(self) -> None:
        existing = self.execute("SELECT username FROM login WHERE username = %s", ("admin",)).fetchone()
        if existing is None:
            self.execute(
                "INSERT INTO login (username, password, role) VALUES (%s, %s, %s)",
                ("admin", "admin123", "admin"),
            )
            self.commit()

    def list_tables(self):
        if self.use_sqlite:
            rows = self.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            ).fetchall()
            return [row[0] for row in rows]

        rows = self.execute("SHOW TABLES").fetchall()
        return [next(iter(row.values())) for row in rows]

    def close(self) -> None:
        self.connection.close()
