# Banking Management System

A desktop banking management system built with Python and a MySQL-ready backend for interviews and portfolio projects.

## Features
- Create customer accounts
- Deposit money
- Withdraw money
- Transfer money
- View transaction statements
- MySQL schema support for real database usage

## MySQL setup
1. Create a MySQL database and user.
2. Run the SQL script:
   ```bash
   mysql -u root -p < mysql_setup.sql
   ```
3. Set environment variables if needed:
   ```bash
   set DB_HOST=localhost
   set DB_USER=root
   set DB_PASSWORD=your_password
   set DB_NAME=bank_db
   ```

## Run
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Run the tests:
   ```bash
   python -m unittest discover -s tests -v
   ```
