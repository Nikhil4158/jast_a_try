def get_statement(db, account_no):
    rows = db.execute(
        "SELECT transaction_type, amount, balance_after, transaction_date FROM transactions WHERE account_no = %s ORDER BY transaction_id DESC",
        (account_no,),
    ).fetchall()
    return [dict(row) for row in rows]
