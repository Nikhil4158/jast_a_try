from datetime import datetime


def withdraw_money(db, account_no, amount):
    amount = float(amount)
    if amount <= 0:
        raise ValueError("Withdraw amount must be positive")

    current = db.execute("SELECT balance FROM customers WHERE account_no = %s", (account_no,)).fetchone()
    if current is None:
        raise ValueError("Account not found")

    current_balance = float(current["balance"])
    if current_balance < amount:
        raise ValueError("Insufficient balance")

    new_balance = current_balance - amount
    db.execute("UPDATE customers SET balance = %s WHERE account_no = %s", (new_balance, account_no))
    db.execute(
        "INSERT INTO transactions (account_no, transaction_type, amount, balance_after, transaction_date) VALUES (%s, %s, %s, %s, %s)",
        (account_no, "Withdrawal", amount, new_balance, datetime.now().isoformat(timespec="seconds")),
    )
    db.commit()
    return new_balance
