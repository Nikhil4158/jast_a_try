def _next_account_number(db) -> int:
    row = db.execute("SELECT MAX(account_no) AS max_account FROM customers").fetchone()
    max_account = row["max_account"] if row is not None else 0
    return int(max_account or 100000000) + 1


def create_customer(db, name, email, phone, address, account_type, initial_balance=0.0, ifsc_code=None):
    account_no = _next_account_number(db)
    ifsc_code = ifsc_code or "BKID0001001"
    db.execute(
        "INSERT INTO customers (account_no, ifsc_code, name, email, phone, address, account_type, balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (account_no, ifsc_code, name, email, phone, address, account_type, float(initial_balance)),
    )
    db.commit()
    return account_no


def get_customer_details(db, account_no):
    row = db.execute(
        "SELECT * FROM customers WHERE account_no = %s",
        (account_no,),
    ).fetchone()
    if row is None:
        return None
    return dict(row)


def update_customer(db, account_no, name=None, email=None, phone=None, address=None, account_type=None):
    updates = []
    values = []
    if name is not None:
        updates.append("name = %s")
        values.append(name)
    if email is not None:
        updates.append("email = %s")
        values.append(email)
    if phone is not None:
        updates.append("phone = %s")
        values.append(phone)
    if address is not None:
        updates.append("address = %s")
        values.append(address)
    if account_type is not None:
        updates.append("account_type = %s")
        values.append(account_type)

    if not updates:
        return False

    values.append(account_no)
    db.execute(f"UPDATE customers SET {', '.join(updates)} WHERE account_no = %s", values)
    db.commit()
    return True


def delete_customer(db, account_no):
    db.execute("DELETE FROM customers WHERE account_no = %s", (account_no,))
    db.commit()
    return True
