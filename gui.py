import tkinter as tk
from tkinter import messagebox
import re
import mysql.connector
from function import login_user, signup_user
from schema import create_table
from seed_data import seed_users, seed_employees, seed_trains, seed_bookings
from config import connection

cursor = connection.cursor()

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def open_gui():
    def login_user_gui():
        username = entry_username.get()
        password = entry_password.get()
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Login", "Login Successful!")
        else:
            messagebox.showerror("Login", "Invalid credentials!")

    def signup_user_gui():
        username = entry_signup_username.get()
        password = entry_signup_password.get()
        email = entry_signup_email.get()
        if not validate_email(email):
            messagebox.showerror("Signup", "Invalid email format!")
            return
        try:
            signup_user(username, password, email)
            messagebox.showinfo("Signup", "Signup Successful!")
        except mysql.connector.Error as err:
            messagebox.showerror("Signup", f"Error: {err}")

    def view_schedule_gui():
        schedule_window = tk.Toplevel(root)
        schedule_window.title("Train Schedule")
        try:
            cursor.execute("SELECT * FROM trains")
            trains = cursor.fetchall()
            for idx, train in enumerate(trains):
                info = f"{train[1]} - {train[2]} ({train[3]} → {train[4]}) @ {train[5]}"
                tk.Label(schedule_window, text=info).grid(row=idx, column=0, sticky="w")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load schedule: {err}")

    root = tk.Tk()
    root.title("Railway Reservation System")

    # --- Login Frame ---
    login_frame = tk.LabelFrame(root, text="User Login", padx=10, pady=10)
    login_frame.grid(row=0, column=0, padx=10, pady=10)

    tk.Label(login_frame, text="Username").grid(row=0, column=0)
    entry_username = tk.Entry(login_frame)
    entry_username.grid(row=0, column=1)

    tk.Label(login_frame, text="Password").grid(row=1, column=0)
    entry_password = tk.Entry(login_frame, show="*")
    entry_password.grid(row=1, column=1)

    tk.Button(login_frame, text="Login", command=login_user_gui).grid(row=2, columnspan=2, pady=5)

    # --- Signup Frame ---
    signup_frame = tk.LabelFrame(root, text="User Signup", padx=10, pady=10)
    signup_frame.grid(row=1, column=0, padx=10, pady=10)

    tk.Label(signup_frame, text="Username").grid(row=0, column=0)
    entry_signup_username = tk.Entry(signup_frame)
    entry_signup_username.grid(row=0, column=1)

    tk.Label(signup_frame, text="Password").grid(row=1, column=0)
    entry_signup_password = tk.Entry(signup_frame, show="*")
    entry_signup_password.grid(row=1, column=1)

    tk.Label(signup_frame, text="Email").grid(row=2, column=0)
    entry_signup_email = tk.Entry(signup_frame)
    entry_signup_email.grid(row=2, column=1)

    tk.Button(signup_frame, text="Signup", command=signup_user_gui).grid(row=3, columnspan=2, pady=5)

    # --- View Schedule Button ---
    tk.Button(root, text="View Train Schedule", command=view_schedule_gui, bg="lightblue").grid(row=2, column=0, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_table()
    seed_users()
    seed_employees()
    seed_trains()
    seed_bookings()
    open_gui()  # Launch GUI (replaces terminal interface)
