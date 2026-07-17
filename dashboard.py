import tkinter as tk
from tkinter import messagebox, ttk

from customer import create_customer, get_customer_details
from deposit import deposit_money
from withdraw import withdraw_money
from transfer import transfer_money
from statement import get_statement
from database import DEFAULT_IFSC_CODE


def show_dashboard(root, db):
    dashboard = tk.Toplevel(root)
    dashboard.title("Bank Management System")
    dashboard.geometry("900x650")
    dashboard.configure(bg="#f3f6fb")
    dashboard.transient(root)
    dashboard.grab_set()

    tk.Label(
        dashboard,
        text="BANK MANAGEMENT SYSTEM",
        font=("Segoe UI", 22, "bold"),
        bg="#f3f6fb",
        fg="#0f4c81",
    ).pack(pady=(20, 5))

    tk.Label(
        dashboard,
        text="Admin Dashboard",
        font=("Segoe UI", 12),
        bg="#f3f6fb",
        fg="#5c6b7a",
    ).pack(pady=(0, 20))

    def open_create_account_window():
        win = tk.Toplevel(dashboard)
        win.title("Create Account")
        win.geometry("540x420")
        win.transient(dashboard)
        win.grab_set()

        tk.Label(win, text="CREATE NEW ACCOUNT", font=("Segoe UI", 16, "bold"), fg="#0f4c81").pack(pady=(16, 8))

        form_frame = tk.Frame(win)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        name_var = tk.StringVar()
        email_var = tk.StringVar()
        phone_var = tk.StringVar()
        address_var = tk.StringVar()
        account_type_var = tk.StringVar(value="Savings")
        balance_var = tk.StringVar(value="0")
        account_no_var = tk.StringVar(value="Auto-generated after creation")
        ifsc_var = tk.StringVar(value=DEFAULT_IFSC_CODE)

        def handle_create_account():
            try:
                account_no = create_customer(
                    db,
                    name=name_var.get().strip(),
                    email=email_var.get().strip(),
                    phone=phone_var.get().strip(),
                    address=address_var.get().strip(),
                    account_type=account_type_var.get(),
                    initial_balance=float(balance_var.get()),
                    ifsc_code=ifsc_var.get().strip() or DEFAULT_IFSC_CODE,
                )
                customer = get_customer_details(db, account_no)
                account_no_var.set(f"{account_no}")
                ifsc_var.set(customer.get("ifsc_code", DEFAULT_IFSC_CODE) if customer else DEFAULT_IFSC_CODE)
                messagebox.showinfo(
                    "Success",
                    "Account created successfully.\n\n"
                    f"Account Number : {account_no}\n"
                    f"IFSC Code      : {ifsc_var.get()}\n"
                    f"Customer Name  : {name_var.get().strip()}\n"
                    f"Opening Balance: {balance_var.get()}",
                )
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        def add_form_row(label_text, variable, entry_type="entry"):
            row = tk.Frame(form_frame)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label_text, width=18, anchor="w").pack(side="left")
            if entry_type == "entry":
                tk.Entry(row, textvariable=variable, width=28).pack(side="left")
            else:
                ttk.Combobox(row, textvariable=variable, values=["Savings", "Current", "Fixed"], state="readonly", width=25).pack(side="left")

        add_form_row("Customer Name", name_var)
        add_form_row("Email", email_var)
        add_form_row("Phone Number", phone_var)
        add_form_row("Address", address_var)
        add_form_row("Account Type", account_type_var, entry_type="combo")
        add_form_row("Opening Balance", balance_var)

        row = tk.Frame(form_frame)
        row.pack(fill="x", pady=4)
        tk.Label(row, text="Account Number", width=18, anchor="w").pack(side="left")
        tk.Entry(row, textvariable=account_no_var, width=28, state="readonly").pack(side="left")

        row = tk.Frame(form_frame)
        row.pack(fill="x", pady=4)
        tk.Label(row, text="IFSC Code", width=18, anchor="w").pack(side="left")
        tk.Entry(row, textvariable=ifsc_var, width=28, state="readonly").pack(side="left")

        tk.Button(win, text="Create Account", command=handle_create_account, bg="#0f4c81", fg="white", width=20).pack(pady=10)

    def open_deposit_window():
        win = tk.Toplevel(dashboard)
        win.title("Deposit")
        win.geometry("420x250")
        win.transient(dashboard)
        win.grab_set()

        tk.Label(win, text="DEPOSIT MONEY", font=("Segoe UI", 16, "bold"), fg="#0f4c81").pack(pady=(16, 10))
        account_var = tk.StringVar()
        amount_var = tk.StringVar()

        def handle_deposit():
            try:
                deposit_money(db, int(account_var.get()), float(amount_var.get()))
                messagebox.showinfo("Success", "Money deposited successfully")
                win.destroy()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Label(win, text="Account Number").pack(anchor="w", padx=25)
        tk.Entry(win, textvariable=account_var).pack(padx=25, pady=2, fill="x")
        tk.Label(win, text="Amount").pack(anchor="w", padx=25, pady=(8, 0))
        tk.Entry(win, textvariable=amount_var).pack(padx=25, pady=2, fill="x")
        tk.Button(win, text="Deposit", command=handle_deposit, bg="#0f4c81", fg="white", width=20).pack(pady=16)

    def open_withdraw_window():
        win = tk.Toplevel(dashboard)
        win.title("Withdraw")
        win.geometry("420x250")
        win.transient(dashboard)
        win.grab_set()

        tk.Label(win, text="WITHDRAW MONEY", font=("Segoe UI", 16, "bold"), fg="#0f4c81").pack(pady=(16, 10))
        account_var = tk.StringVar()
        amount_var = tk.StringVar()

        def handle_withdraw():
            try:
                withdraw_money(db, int(account_var.get()), float(amount_var.get()))
                messagebox.showinfo("Success", "Money withdrawn successfully")
                win.destroy()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Label(win, text="Account Number").pack(anchor="w", padx=25)
        tk.Entry(win, textvariable=account_var).pack(padx=25, pady=2, fill="x")
        tk.Label(win, text="Amount").pack(anchor="w", padx=25, pady=(8, 0))
        tk.Entry(win, textvariable=amount_var).pack(padx=25, pady=2, fill="x")
        tk.Button(win, text="Withdraw", command=handle_withdraw, bg="#0f4c81", fg="white", width=20).pack(pady=16)

    def open_transfer_window():
        win = tk.Toplevel(dashboard)
        win.title("Transfer")
        win.geometry("460x310")
        win.transient(dashboard)
        win.grab_set()
        tk.Label(win, text="TRANSFER MONEY", font=("Segoe UI", 16, "bold"), fg="#0f4c81").pack(pady=(16, 10))

        sender_var = tk.StringVar()
        receiver_var = tk.StringVar()
        amount_var = tk.StringVar()

        def handle_transfer():
            try:
                transfer_money(db, int(sender_var.get()), int(receiver_var.get()), float(amount_var.get()))
                messagebox.showinfo("Success", "Transfer completed successfully")
                win.destroy()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Label(win, text="Sender Account Number").pack(anchor="w", padx=25)
        tk.Entry(win, textvariable=sender_var).pack(padx=25, pady=2, fill="x")
        tk.Label(win, text="Receiver Account Number").pack(anchor="w", padx=25, pady=(8, 0))
        tk.Entry(win, textvariable=receiver_var).pack(padx=25, pady=2, fill="x")
        tk.Label(win, text="Transfer Amount").pack(anchor="w", padx=25, pady=(8, 0))
        tk.Entry(win, textvariable=amount_var).pack(padx=25, pady=2, fill="x")
        tk.Button(win, text="Transfer", command=handle_transfer, bg="#0f4c81", fg="white", width=20).pack(pady=16)

    def open_balance_inquiry_window():
        win = tk.Toplevel(dashboard)
        win.title("Balance Inquiry")
        win.geometry("460x320")
        win.transient(dashboard)
        win.grab_set()
        tk.Label(win, text="BALANCE INQUIRY", font=("Segoe UI", 16, "bold"), fg="#0f4c81").pack(pady=(16, 10))

        account_var = tk.StringVar()
        name_var = tk.StringVar(value="")
        type_var = tk.StringVar(value="")
        balance_var = tk.StringVar(value="")
        ifsc_var = tk.StringVar(value="")

        def handle_search():
            try:
                customer = get_customer_details(db, int(account_var.get()))
                if customer is None:
                    messagebox.showerror("Not Found", "No account found for this number")
                    return
                name_var.set(customer.get("name", ""))
                type_var.set(customer.get("account_type", ""))
                balance_var.set(f"{float(customer.get('balance', 0.0)):.2f}")
                ifsc_var.set(customer.get("ifsc_code", DEFAULT_IFSC_CODE))
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Label(win, text="Account Number").pack(anchor="w", padx=25)
        tk.Entry(win, textvariable=account_var).pack(padx=25, pady=2, fill="x")
        tk.Button(win, text="Search", command=handle_search, bg="#0f4c81", fg="white", width=20).pack(pady=12)

        tk.Label(win, text="Customer Name").pack(anchor="w", padx=25)
        tk.Entry(win, textvariable=name_var, state="readonly").pack(padx=25, pady=2, fill="x")
        tk.Label(win, text="Account Type").pack(anchor="w", padx=25, pady=(8, 0))
        tk.Entry(win, textvariable=type_var, state="readonly").pack(padx=25, pady=2, fill="x")
        tk.Label(win, text="Current Balance").pack(anchor="w", padx=25, pady=(8, 0))
        tk.Entry(win, textvariable=balance_var, state="readonly").pack(padx=25, pady=2, fill="x")
        tk.Label(win, text="IFSC Code").pack(anchor="w", padx=25, pady=(8, 0))
        tk.Entry(win, textvariable=ifsc_var, state="readonly").pack(padx=25, pady=2, fill="x")

    def open_statement_window():
        win = tk.Toplevel(dashboard)
        win.title("Statement")
        win.geometry("420x240")
        win.transient(dashboard)
        win.grab_set()
        tk.Label(win, text="ACCOUNT STATEMENT", font=("Segoe UI", 16, "bold"), fg="#0f4c81").pack(pady=(16, 10))

        account_var = tk.StringVar()

        def handle_statement():
            try:
                rows = get_statement(db, int(account_var.get()))
                body = "\n".join([f"{row['transaction_type']} | {row['amount']} | {row['balance_after']} | {row['transaction_date']}" for row in rows])
                messagebox.showinfo("Statement", body or "No transactions found")
                win.destroy()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Label(win, text="Account Number").pack(anchor="w", padx=25)
        tk.Entry(win, textvariable=account_var).pack(padx=25, pady=2, fill="x")
        tk.Button(win, text="Show Statement", command=handle_statement, bg="#0f4c81", fg="white", width=20).pack(pady=16)

    section_frame = tk.Frame(dashboard, bg="#ffffff", bd=1, relief="groove")
    section_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    def add_button(text, command, bg="#0f4c81"):
        tk.Button(section_frame, text=text, width=24, height=2, command=command, bg=bg, fg="white", font=("Segoe UI", 11, "bold"), relief="flat").pack(pady=5)

    add_button("Create Account", open_create_account_window)
    add_button("Deposit", open_deposit_window)
    add_button("Withdraw", open_withdraw_window)
    add_button("Transfer", open_transfer_window)
    add_button("Balance Inquiry", open_balance_inquiry_window)
    add_button("Statement", open_statement_window)

    tk.Button(dashboard, text="Logout", command=lambda: dashboard.destroy(), bg="#c0392b", fg="white", width=16).pack(pady=10)
