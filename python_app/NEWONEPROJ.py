import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime 


# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect("cybercrime.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    role TEXT DEFAULT 'user'
)
""")

# Complaints table
cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    crime_type TEXT,
    incident_date TEXT,
    description TEXT,
    financial_loss REAL,
    status TEXT DEFAULT 'Pending',
    created_at TEXT
)
""")

# Evidence table
cursor.execute("""
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id INTEGER,
    evidence_type TEXT,
    description TEXT
)
""")

conn.commit()


# Create default admin
cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    ("admin",)
)

if cursor.fetchone() is None:
    cursor.execute("""
        INSERT INTO users
        (name, username, password, email, role)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "Administrator",
        "admin",
        "admin123",
        "admin@cyber.com",
        "admin"
    ))

    conn.commit()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Cybercrime Incident Reporting System")
root.geometry("900x600")


# =========================================================
# CLEAR WINDOW
# =========================================================

def clear_window():

    for widget in root.winfo_children():
        widget.destroy()


# =========================================================
# REGISTER
# =========================================================

def register_page():

    clear_window()

    tk.Label(
        root,
        text="USER REGISTRATION",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text="Name").grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(frame, width=30)
    name_entry.grid(row=0, column=1)

    tk.Label(frame, text="Username").grid(row=1, column=0, padx=10, pady=10)
    username_entry = tk.Entry(frame, width=30)
    username_entry.grid(row=1, column=1)

    tk.Label(frame, text="Email").grid(row=2, column=0, padx=10, pady=10)
    email_entry = tk.Entry(frame, width=30)
    email_entry.grid(row=2, column=1)

    tk.Label(frame, text="Password").grid(row=3, column=0, padx=10, pady=10)
    password_entry = tk.Entry(frame, width=30, show="*")
    password_entry.grid(row=3, column=1)

    tk.Label(frame, text="Confirm Password").grid(
        row=4,
        column=0,
        padx=10,
        pady=10
    )

    confirm_entry = tk.Entry(frame, width=30, show="*")
    confirm_entry.grid(row=4, column=1)

    def register():

        name = name_entry.get()
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm = confirm_entry.get()

        if not name or not username or not email or not password:
            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Error",
                "Passwords do not match."
            )
            return

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        if cursor.fetchone():
            messagebox.showerror(
                "Error",
                "Username already exists. Please login."
            )
            return

        cursor.execute("""
            INSERT INTO users
            (name, username, password, email, role)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            username,
            password,
            email,
            "user"
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Registration successful! Please login."
        )

        login_page()

    tk.Button(
        root,
        text="REGISTER",
        width=20,
        command=register
    ).pack(pady=10)

    tk.Button(
        root,
        text="BACK TO LOGIN",
        command=login_page
    ).pack()


# =========================================================
# LOGIN
# =========================================================

def login_page():

    clear_window()

    # COLORFUL FRONT PAGE ONLY
    root.configure(bg="#EAF4FF")

    header = tk.Frame(root, bg="#123C69", height=120)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="CYBERCRIME",
        font=("Arial", 28, "bold"),
        bg="#123C69",
        fg="white"
    ).pack(pady=(18, 0))

    tk.Label(
        header,
        text="INCIDENT REPORTING SYSTEM",
        font=("Arial", 15, "bold"),
        bg="#123C69",
        fg="#BFE7FF"
    ).pack(pady=5)

    tk.Label(
        root,
        text="Welcome",
        font=("Arial", 25, "bold"),
        bg="#EAF4FF",
        fg="#123C69"
    ).pack(pady=(25, 3))

    tk.Label(
        root,
        text="Report cybercrime incidents securely and track your complaints",
        font=("Arial", 11),
        bg="#EAF4FF",
        fg="#4A5568"
    ).pack()

    card = tk.Frame(
        root,
        bg="white",
        bd=1,
        relief="solid",
        padx=35,
        pady=25
    )
    card.pack(pady=20)

    tk.Label(
        card,
        text="User Login",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#123C69"
    ).grid(row=0, column=0, columnspan=2, pady=(0, 18))

    tk.Label(
        card,
        text="Username",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#333333"
    ).grid(row=1, column=0, sticky="w", padx=8, pady=8)

    username_entry = tk.Entry(
        card, width=30, font=("Arial", 11), relief="solid", bd=1
    )
    username_entry.grid(row=1, column=1, padx=8, pady=8)

    tk.Label(
        card,
        text="Password",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#333333"
    ).grid(row=2, column=0, sticky="w", padx=8, pady=8)

    password_entry = tk.Entry(
        card, width=30, font=("Arial", 11), show="*",
        relief="solid", bd=1
    )
    password_entry.grid(row=2, column=1, padx=8, pady=8)

    def login():
        username = username_entry.get()
        password = password_entry.get()

        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        user = cursor.fetchone()

        if user:
            if user[5] == "admin":
                admin_dashboard()
            else:
                user_dashboard(username, user[1])
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    tk.Button(
        card,
        text="LOGIN",
        width=25,
        font=("Arial", 11, "bold"),
        bg="#1F7A8C",
        fg="white",
        activebackground="#145A67",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=login
    ).grid(row=3, column=0, columnspan=2, pady=(18, 8))

    tk.Button(
        card,
        text="CREATE NEW ACCOUNT",
        width=25,
        font=("Arial", 10, "bold"),
        bg="#2A9D8F",
        fg="white",
        activebackground="#217A70",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=register_page
    ).grid(row=4, column=0, columnspan=2, pady=5)

    tk.Button(
        root,
        text="ADMIN LOGIN",
        width=20,
        font=("Arial", 10, "bold"),
        bg="#E76F51",
        fg="white",
        activebackground="#C9573D",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=admin_login_page
    ).pack(pady=5)

    tk.Label(
        root,
        text="Secure  •  Simple  •  Fast",
        font=("Arial", 10, "italic"),
        bg="#EAF4FF",
        fg="#667085"
    ).pack(pady=8)


# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login_page():

    clear_window()

    tk.Label(
        root,
        text="ADMIN LOGIN",
        font=("Arial", 24, "bold")
    ).pack(pady=30)

    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text="Admin Username").grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    username_entry = tk.Entry(frame, width=30)
    username_entry.grid(row=0, column=1)

    tk.Label(frame, text="Admin Password").grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    password_entry = tk.Entry(
        frame,
        width=30,
        show="*"
    )

    password_entry.grid(row=1, column=1)

    def admin_login():

        username = username_entry.get()
        password = password_entry.get()

        cursor.execute("""
            SELECT * FROM users
            WHERE username = ?
            AND password = ?
            AND role = 'admin'
        """, (username, password))

        result = cursor.fetchone()

        if result:

            admin_dashboard()

        else:

            messagebox.showerror(
                "Error",
                "Invalid admin credentials."
            )

    tk.Button(
        root,
        text="ADMIN LOGIN",
        width=20,
        command=admin_login
    ).pack(pady=10)

    tk.Button(
        root,
        text="BACK",
        command=login_page
    ).pack()


# =========================================================
# USER DASHBOARD
# =========================================================

def user_dashboard(username, name):

    clear_window()

    # =====================================================
    # USER DASHBOARD - EQUAL SIZE WIDGET DESIGN
    # =====================================================
    root.configure(bg="#EEF5FB")

    # Header
    header = tk.Frame(root, bg="#123C69", height=105)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text=f"Welcome, {name}!",
        font=("Arial", 25, "bold"),
        bg="#123C69",
        fg="white"
    ).pack(pady=(18, 2))

    tk.Label(
        header,
        text="Cybercrime Incident Reporting System",
        font=("Arial", 11),
        bg="#123C69",
        fg="#BFE7FF"
    ).pack()

    # Page title
    tk.Label(
        root,
        text="USER DASHBOARD",
        font=("Arial", 20, "bold"),
        bg="#EEF5FB",
        fg="#123C69"
    ).pack(pady=(22, 3))

    tk.Label(
        root,
        text="Choose an option to manage your cybercrime complaints",
        font=("Arial", 10),
        bg="#EEF5FB",
        fg="#667085"
    ).pack(pady=(0, 14))

    # FIXED WIDGET AREA - EXACTLY THE SAME SIZE
    widgets_frame = tk.Frame(
        root,
        bg="#EEF5FB",
        width=680,
        height=360
    )
    widgets_frame.pack()
    widgets_frame.pack_propagate(False)
    widgets_frame.grid_propagate(False)

    # Each grid cell is exactly the same size
    widgets_frame.grid_columnconfigure(0, minsize=340, weight=0)
    widgets_frame.grid_columnconfigure(1, minsize=340, weight=0)
    widgets_frame.grid_rowconfigure(0, minsize=180, weight=0)
    widgets_frame.grid_rowconfigure(1, minsize=180, weight=0)

    def make_widget(parent, row, column, icon, title, description,
                    command, bg_color):

        # EXACT SAME SIZE FOR EVERY WIDGET
        widget = tk.Frame(
            parent,
            bg="white",
            width=320,
            height=160,
            bd=1,
            relief="solid",
            cursor="hand2"
        )
        widget.grid(
            row=row,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        widget.grid_propagate(False)

        # Small colored top line
        top_line = tk.Frame(
            widget,
            bg=bg_color,
            height=5
        )
        top_line.pack(fill="x")
        top_line.pack_propagate(False)

        # Icon
        icon_label = tk.Label(
            widget,
            text=icon,
            font=("Arial", 23, "bold"),
            bg=bg_color,
            fg="white",
            width=3,
            height=1
        )
        icon_label.pack(pady=(10, 5))

        # Title
        title_label = tk.Label(
            widget,
            text=title,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#123C69"
        )
        title_label.pack()

        # Description
        desc_label = tk.Label(
            widget,
            text=description,
            font=("Arial", 9),
            bg="white",
            fg="#667085",
            wraplength=260,
            justify="center"
        )
        desc_label.pack(pady=(4, 5))

        # Click only - NO HOVER EFFECT
        def click(event=None):
            command()

        for item in (widget, top_line, icon_label, title_label, desc_label):
            item.bind("<Button-1>", click)

    # Row 1
    make_widget(
        widgets_frame, 0, 0,
        "!", "REPORT CYBERCRIME",
        "Submit a new cybercrime complaint",
        lambda: report_crime(username),
        "#1F7A8C"
    )

    make_widget(
        widgets_frame, 0, 1,
        "C", "MY COMPLAINTS",
        "View all your submitted complaints",
        lambda: my_complaints(username),
        "#2A9D8F"
    )

    # Row 2
    make_widget(
        widgets_frame, 1, 0,
        "?", "TRACK COMPLAINT",
        "Check the current complaint status",
        lambda: track_complaint(username),
        "#457B9D"
    )

    make_widget(
        widgets_frame, 1, 1,
        "X", "LOGOUT",
        "Return safely to the login page",
        login_page,
        "#E76F51"
    )

    # Footer
    tk.Label(
        root,
        text="Secure  •  Simple  •  Fast",
        font=("Arial", 9, "italic"),
        bg="#EEF5FB",
        fg="#667085"
    ).pack(pady=7)



# =========================================================
# REPORT CYBERCRIME
# =========================================================

def report_crime(username):

    clear_window()

    tk.Label(
        root,
        text="REPORT CYBERCRIME",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(
        frame,
        text="Crime Type"
    ).grid(row=0, column=0, padx=10, pady=10)

    crime_box = ttk.Combobox(
        frame,
        values=[
            "Phishing",
            "UPI Fraud",
            "Online Banking Fraud",
            "Cyberbullying",
            "Identity Theft",
            "Social Media Hacking",
            "Fake Website",
            "Online Shopping Fraud",
            "Email Scam",
            "Other"
        ],
        width=28
    )

    crime_box.grid(row=0, column=1)

    tk.Label(
        frame,
        text="Incident Date"
    ).grid(row=1, column=0, padx=10, pady=10)

    date_entry = tk.Entry(frame, width=30)
    date_entry.grid(row=1, column=1)

    tk.Label(
        frame,
        text="Financial Loss"
    ).grid(row=2, column=0, padx=10, pady=10)

    loss_entry = tk.Entry(frame, width=30)
    loss_entry.grid(row=2, column=1)

    tk.Label(
        frame,
        text="Description"
    ).grid(row=3, column=0, padx=10, pady=10)

    description = tk.Text(
        frame,
        width=30,
        height=6
    )

    description.grid(row=3, column=1)

    def submit():

        crime = crime_box.get()
        date = date_entry.get()
        loss = loss_entry.get()
        desc = description.get("1.0", tk.END)

        if not crime or not date or not desc.strip():
            messagebox.showwarning(
                "Warning",
                "Please fill the required fields."
            )
            return

        try:
            loss = float(loss) if loss else 0

        except ValueError:

            messagebox.showerror(
                "Error",
                "Financial loss must be a number."
            )
            return

        created = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO complaints
            (username, crime_type, incident_date,
             description, financial_loss,
             status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            crime,
            date,
            desc,
            loss,
            "Pending",
            created
        ))

        conn.commit()

        complaint_id = cursor.lastrowid

        messagebox.showinfo(
            "Success",
            f"Complaint submitted successfully!\n\n"
            f"Complaint ID: CR{complaint_id:05d}"
        )

        user_dashboard(username, username)

    tk.Button(
        root,
        text="SUBMIT COMPLAINT",
        width=25,
        command=submit
    ).pack(pady=10)

    tk.Button(
        root,
        text="BACK",
        command=lambda: user_dashboard(username, username)
    ).pack()


# =========================================================
# MY COMPLAINTS
# =========================================================

def my_complaints(username):

    clear_window()

    tk.Label(
        root,
        text="MY COMPLAINTS",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    columns = (
        "ID",
        "Crime Type",
        "Date",
        "Loss",
        "Status"
    )

    tree = ttk.Treeview(
        root,
        columns=columns,
        show="headings"
    )

    for col in columns:

        tree.heading(col, text=col)
        tree.column(col, width=140)

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    cursor.execute("""
        SELECT complaint_id,
               crime_type,
               incident_date,
               financial_loss,
               status
        FROM complaints
        WHERE username = ?
    """, (username,))

    rows = cursor.fetchall()

    for row in rows:

        tree.insert(
            "",
            tk.END,
            values=(
                f"CR{row[0]:05d}",
                row[1],
                row[2],
                row[3],
                row[4]
            )
        )

    tk.Button(
        root,
        text="BACK",
        command=lambda: user_dashboard(username, username)
    ).pack(pady=10)


# =========================================================
# TRACK COMPLAINT
# =========================================================

def track_complaint(username):

    clear_window()

    tk.Label(
        root,
        text="TRACK COMPLAINT",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    tk.Label(
        root,
        text="Enter Complaint ID"
    ).pack()

    entry = tk.Entry(root, width=30)
    entry.pack(pady=10)

    result_label = tk.Label(
        root,
        text="",
        font=("Arial", 12)
    )

    result_label.pack(pady=20)

    def track():

        value = entry.get().replace(
            "CR",
            ""
        )

        try:
            complaint_id = int(value)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid Complaint ID."
            )
            return

        cursor.execute("""
            SELECT crime_type,
                   incident_date,
                   description,
                   status
            FROM complaints
            WHERE complaint_id = ?
            AND username = ?
        """, (
            complaint_id,
            username
        ))

        row = cursor.fetchone()

        if row:

            result_label.config(
                text=
                f"Crime Type: {row[0]}\n"
                f"Incident Date: {row[1]}\n"
                f"Description: {row[2]}\n"
                f"Status: {row[3]}"
            )

        else:

            result_label.config(
                text="Complaint not found."
            )

    tk.Button(
        root,
        text="TRACK",
        command=track
    ).pack()

    tk.Button(
        root,
        text="BACK",
        command=lambda: user_dashboard(username, username)
    ).pack(pady=20)


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard():

    clear_window()

    # =====================================================
    # ADMIN DASHBOARD - EQUAL SIZE WIDGET DESIGN
    # =====================================================
    root.configure(bg="#EEF5FB")

    # Header
    header = tk.Frame(root, bg="#123C69", height=105)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="ADMIN DASHBOARD",
        font=("Arial", 25, "bold"),
        bg="#123C69",
        fg="white"
    ).pack(pady=(20, 2))

    tk.Label(
        header,
        text="Cybercrime Incident Reporting System",
        font=("Arial", 11),
        bg="#123C69",
        fg="#BFE7FF"
    ).pack()

    # Page title
    tk.Label(
        root,
        text="ADMIN CONTROL CENTER",
        font=("Arial", 20, "bold"),
        bg="#EEF5FB",
        fg="#123C69"
    ).pack(pady=(22, 3))

    tk.Label(
        root,
        text="Select a widget to manage complaints, evidence and analysis",
        font=("Arial", 10),
        bg="#EEF5FB",
        fg="#667085"
    ).pack(pady=(0, 14))

    # FIXED WIDGET AREA - EXACTLY THE SAME SIZE
    widgets_frame = tk.Frame(
        root,
        bg="#EEF5FB",
        width=680,
        height=360
    )
    widgets_frame.pack()
    widgets_frame.pack_propagate(False)
    widgets_frame.grid_propagate(False)

    # Each grid cell is exactly the same size
    widgets_frame.grid_columnconfigure(0, minsize=340, weight=0)
    widgets_frame.grid_columnconfigure(1, minsize=340, weight=0)
    widgets_frame.grid_rowconfigure(0, minsize=180, weight=0)
    widgets_frame.grid_rowconfigure(1, minsize=180, weight=0)

    def make_widget(parent, row, column, icon, title, description,
                    command, bg_color):

        # EXACT SAME SIZE FOR EVERY WIDGET
        widget = tk.Frame(
            parent,
            bg="white",
            width=320,
            height=160,
            bd=1,
            relief="solid",
            cursor="hand2"
        )
        widget.grid(
            row=row,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        widget.grid_propagate(False)

        # Colored top line
        top_line = tk.Frame(
            widget,
            bg=bg_color,
            height=5
        )
        top_line.pack(fill="x")
        top_line.pack_propagate(False)

        # Icon
        icon_label = tk.Label(
            widget,
            text=icon,
            font=("Arial", 23, "bold"),
            bg=bg_color,
            fg="white",
            width=3,
            height=1
        )
        icon_label.pack(pady=(10, 5))

        # Title
        title_label = tk.Label(
            widget,
            text=title,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#123C69"
        )
        title_label.pack()

        # Description
        desc_label = tk.Label(
            widget,
            text=description,
            font=("Arial", 9),
            bg="white",
            fg="#667085",
            wraplength=260,
            justify="center"
        )
        desc_label.pack(pady=(4, 5))

        # Click only - NO HOVER EFFECT
        def click(event=None):
            command()

        for item in (widget, top_line, icon_label, title_label, desc_label):
            item.bind("<Button-1>", click)

    # Row 1
    make_widget(
        widgets_frame, 0, 0,
        "V", "VIEW COMPLAINTS",
        "View all registered cybercrime cases",
        view_complaints,
        "#1F7A8C"
    )

    make_widget(
        widgets_frame, 0, 1,
        "U", "UPDATE STATUS",
        "Change the status of a complaint",
        update_status,
        "#2A9D8F"
    )

    # Row 2
    make_widget(
        widgets_frame, 1, 0,
        "E", "VIEW EVIDENCE",
        "Review stored digital evidence",
        view_evidence,
        "#457B9D"
    )

    make_widget(
        widgets_frame, 1, 1,
        "A", "DATA ANALYSIS",
        "Analyze cybercrime complaint data",
        analysis_page,
        "#7B61A8"
    )

    # Download complaints stored in the database as CSV
    tk.Button(
        root,
        text="DOWNLOAD COMPLAINTS CSV",
        width=25,
        font=("Arial", 10, "bold"),
        bg="#2A9D8F",
        fg="white",
        activebackground="#217A70",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=download_complaints_csv
    ).pack(pady=5)

    # Logout button
    tk.Button(
        root,
        text="LOGOUT",
        width=20,
        font=("Arial", 10, "bold"),
        bg="#E76F51",
        fg="white",
        activebackground="#C9573D",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=login_page
    ).pack(pady=7)



# =========================================================
# DOWNLOAD COMPLAINTS AS CSV
# =========================================================

def download_complaints_csv():

    cursor.execute("""
        SELECT complaint_id,
               username,
               crime_type,
               incident_date,
               description,
               financial_loss,
               status,
               created_at
        FROM complaints
    """)

    rows = cursor.fetchall()

    if not rows:
        messagebox.showwarning(
            "Warning",
            "No complaint data available to download."
        )
        return

    df = pd.DataFrame(
        rows,
        columns=[
            "Complaint ID",
            "Username",
            "Crime Type",
            "Incident Date",
            "Description",
            "Financial Loss",
            "Status",
            "Created At"
        ]
    )

    # Display Complaint ID in the same CR00001 format used in the application
    df["Complaint ID"] = df["Complaint ID"].apply(
        lambda x: f"CR{x:05d}"
    )

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save Complaints CSV"
    )

    if not file_path:
        return

    df.to_csv(file_path, index=False)

    messagebox.showinfo(
        "Success",
        "Complaint data downloaded successfully as CSV."
    )


# =========================================================
# VIEW COMPLAINTS
# =========================================================

def view_complaints():

    clear_window()

    tk.Label(
        root,
        text="ALL CYBERCRIME COMPLAINTS",
        font=("Arial", 22, "bold")
    ).pack(pady=15)

    columns = (
        "ID",
        "Username",
        "Crime",
        "Date",
        "Loss",
        "Status"
    )

    tree = ttk.Treeview(
        root,
        columns=columns,
        show="headings"
    )

    for col in columns:

        tree.heading(col, text=col)
        tree.column(col, width=130)

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    cursor.execute("""
        SELECT complaint_id,
               username,
               crime_type,
               incident_date,
               financial_loss,
               status
        FROM complaints
    """)

    for row in cursor.fetchall():

        tree.insert(
            "",
            tk.END,
            values=(
                f"CR{row[0]:05d}",
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            )
        )

    tk.Button(
        root,
        text="BACK",
        command=admin_dashboard
    ).pack(pady=10)


# =========================================================
# UPDATE STATUS
# =========================================================

def update_status():

    clear_window()

    tk.Label(
        root,
        text="UPDATE COMPLAINT STATUS",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    tk.Label(
        root,
        text="Complaint ID"
    ).pack()

    id_entry = tk.Entry(root)
    id_entry.pack(pady=10)

    tk.Label(
        root,
        text="New Status"
    ).pack()

    status_box = ttk.Combobox(
        root,
        values=[
            "Pending",
            "Under Investigation",
            "Resolved",
            "Rejected"
        ]
    )

    status_box.pack(pady=10)

    def update():

        try:

            complaint_id = int(
                id_entry.get().replace("CR", "")
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid Complaint ID."
            )
            return

        status = status_box.get()

        if not status:

            messagebox.showwarning(
                "Warning",
                "Select a status."
            )
            return

        cursor.execute("""
            UPDATE complaints
            SET status = ?
            WHERE complaint_id = ?
        """, (
            status,
            complaint_id
        ))

        conn.commit()

        if cursor.rowcount == 0:

            messagebox.showerror(
                "Error",
                "Complaint not found."
            )

        else:

            messagebox.showinfo(
                "Success",
                "Complaint status updated."
            )

    tk.Button(
        root,
        text="UPDATE",
        command=update
    ).pack(pady=10)

    tk.Button(
        root,
        text="BACK",
        command=admin_dashboard
    ).pack()


# =========================================================
# VIEW EVIDENCE
# =========================================================

def view_evidence():

    clear_window()

    tk.Label(
        root,
        text="DIGITAL EVIDENCE",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    columns = (
        "Evidence ID",
        "Complaint ID",
        "Type",
        "Description"
    )

    tree = ttk.Treeview(
        root,
        columns=columns,
        show="headings"
    )

    for col in columns:

        tree.heading(col, text=col)
        tree.column(col, width=180)

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    cursor.execute("""
        SELECT evidence_id,
               complaint_id,
               evidence_type,
               description
        FROM evidence
    """)

    for row in cursor.fetchall():

        tree.insert(
            "",
            tk.END,
            values=row
        )

    tk.Button(
        root,
        text="BACK",
        command=admin_dashboard
    ).pack()


# =========================================================
# ANALYSIS PAGE
# =========================================================

def analysis_page():

    clear_window()

    tk.Label(
        root,
        text="CYBERCRIME DATA ANALYSIS",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    cursor.execute("""
        SELECT crime_type,
               incident_date,
               financial_loss,
               status
        FROM complaints
    """)

    rows = cursor.fetchall()

    if not rows:

        tk.Label(
            root,
            text="No complaint data available."
        ).pack(pady=30)

        tk.Button(
            root,
            text="BACK",
            command=admin_dashboard
        ).pack()

        return

    df = pd.DataFrame(
        rows,
        columns=[
            "crime_type",
            "incident_date",
            "financial_loss",
            "status"
        ]
    )

    # NumPy calculations

    total_cases = len(df)

    average_loss = np.mean(
        df["financial_loss"]
    )

    maximum_loss = np.max(
        df["financial_loss"]
    )

    resolved_cases = np.sum(
        df["status"] == "Resolved"
    )

    tk.Label(
        root,
        text=f"Total Cases: {total_cases}",
        font=("Arial", 14)
    ).pack(pady=5)

    tk.Label(
        root,
        text=f"Average Financial Loss: ₹{average_loss:.2f}",
        font=("Arial", 14)
    ).pack(pady=5)

    tk.Label(
        root,
        text=f"Maximum Financial Loss: ₹{maximum_loss:.2f}",
        font=("Arial", 14)
    ).pack(pady=5)

    tk.Label(
        root,
        text=f"Resolved Cases: {resolved_cases}",
        font=("Arial", 14)
    ).pack(pady=5)

    # -----------------------------------------------------
    # Charts
    # -----------------------------------------------------

    def crime_chart():

        counts = df["crime_type"].value_counts()

        counts.plot(
            kind="bar",
            title="Cybercrime Cases by Type"
        )

        plt.xlabel("Crime Type")
        plt.ylabel("Number of Cases")
        plt.tight_layout()
        plt.show()

    def status_chart():

        counts = df["status"].value_counts()

        counts.plot(
            kind="pie",
            autopct="%1.1f%%",
            title="Complaint Status"
        )

        plt.ylabel("")
        plt.show()

    def loss_chart():

        data = df.groupby(
            "crime_type"
        )["financial_loss"].sum()

        data.plot(
            kind="bar",
            title="Financial Loss by Crime Type"
        )

        plt.xlabel("Crime Type")
        plt.ylabel("Financial Loss")
        plt.tight_layout()
        plt.show()

    tk.Button(
        root,
        text="CRIME TYPE CHART",
        width=25,
        command=crime_chart
    ).pack(pady=8)

    tk.Button(
        root,
        text="STATUS CHART",
        width=25,
        command=status_chart
    ).pack(pady=8)

    tk.Button(
        root,
        text="FINANCIAL LOSS CHART",
        width=25,
        command=loss_chart
    ).pack(pady=8)

    tk.Button(
        root,
        text="BACK",
        command=admin_dashboard
    ).pack(pady=20)


# =========================================================
# START APPLICATION
# =========================================================

login_page()

root.mainloop()

conn.close()





















