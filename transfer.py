from datetime import datetime


def transfer_money(db, sender_account, receiver_account, amount):
    amount = float(amount)
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")

    sender_row = db.execute("SELECT balance FROM customers WHERE account_no = %s", (sender_account,)).fetchone()
    receiver_row = db.execute("SELECT balance FROM customers WHERE account_no = %s", (receiver_account,)).fetchone()
    if sender_row is None or receiver_row is None:
        raise ValueError("Sender or receiver account not found")

    sender_balance = float(sender_row["balance"])
    if sender_balance < amount:
        raise ValueError("Insufficient balance")

    receiver_balance = float(receiver_row["balance"]) + amount
    sender_new_balance = sender_balance - amount

    db.execute("UPDATE customers SET balance = %s WHERE account_no = %s", (sender_new_balance, sender_account))
    db.execute("UPDATE customers SET balance = %s WHERE account_no = %s", (receiver_balance, receiver_account))
    db.execute(
        "INSERT INTO transactions (account_no, transaction_type, amount, balance_after, transaction_date) VALUES (%s, %s, %s, %s, %s)",
        (sender_account, "Transfer Sent", amount, sender_new_balance, datetime.now().isoformat(timespec="seconds")),
    )
    db.execute(
        "INSERT INTO transactions (account_no, transaction_type, amount, balance_after, transaction_date) VALUES (%s, %s, %s, %s, %s)",
        (receiver_account, "Transfer Received", amount, receiver_balance, datetime.now().isoformat(timespec="seconds")),
    )
    db.execute(
        "INSERT INTO transfers (sender_account, receiver_account, amount, transfer_date) VALUES (%s, %s, %s, %s)",
        (sender_account, receiver_account, amount, datetime.now().isoformat(timespec="seconds")),
    )
    db.commit()
    return sender_new_balance, receiver_balance
