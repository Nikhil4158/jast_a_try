import tkinter as tk
from tkinter import messagebox


def show_login_window(root, on_login_success):
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("420x280")
    login_window.configure(bg="#f3f6fb")
    login_window.transient(root)
    login_window.grab_set()

    tk.Label(
        login_window,
        text="ADMIN LOGIN",
        font=("Segoe UI", 18, "bold"),
        bg="#f3f6fb",
        fg="#0f4c81",
    ).pack(pady=(20, 10))

    tk.Label(login_window, text="Username", bg="#f3f6fb").pack(anchor="w", padx=40)
    username_var = tk.StringVar()
    tk.Entry(login_window, textvariable=username_var, width=30).pack(padx=40, pady=4)

    tk.Label(login_window, text="Password", bg="#f3f6fb").pack(anchor="w", padx=40, pady=(8, 0))
    password_var = tk.StringVar()
    tk.Entry(login_window, textvariable=password_var, width=30, show="*").pack(padx=40, pady=4)

    def handle_login():
        if username_var.get().strip() == "admin" and password_var.get().strip() == "admin123":
            login_window.destroy()
            on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    tk.Button(
        login_window,
        text="Login",
        command=handle_login,
        bg="#0f4c81",
        fg="white",
        width=20,
        height=1,
    ).pack(pady=20)
