import tkinter as tk
from tkinter import messagebox

from database import DatabaseManager
from login import show_login_window
from dashboard import show_dashboard


def build_app():
    db = DatabaseManager(use_sqlite=True)
    db.init_db()
    db.seed_default_admin()

    root = tk.Tk()
    root.title("Banking Management System")
    root.geometry("400x250")
    root.configure(bg="#f3f6fb")

    tk.Label(
        root,
        text="BANKING MANAGEMENT SYSTEM",
        font=("Segoe UI", 20, "bold"),
        bg="#f3f6fb",
        fg="#0f4c81",
    ).pack(pady=(20, 10))

    tk.Label(
        root,
        text="Welcome! Please login to continue",
        bg="#f3f6fb",
        fg="#5c6b7a",
    ).pack(pady=(0, 20))

    def start_dashboard():
        show_dashboard(root, db)

    show_login_window(root, start_dashboard)
    root.mainloop()


def main():
    build_app()


if __name__ == "__main__":
    main()
