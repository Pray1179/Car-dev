import os
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Verstappen@1"),
    "database": os.getenv("DB_NAME", "AutoSpec Database System"),
    "autocommit": True,
}


class CarDealerInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Car Dealership Management System")
        self.geometry("1280x760")
        self.minsize(1100, 650)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.login_frame = ttk.Frame(self.notebook)
        self.inventory_frame = ttk.Frame(self.notebook)
        self.booking_frame = ttk.Frame(self.notebook)
        self.admin_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.login_frame, text="Login")
        self.notebook.add(self.inventory_frame, text="Inventory")
        self.notebook.add(self.booking_frame, text="Bookings")
        self.notebook.add(self.admin_frame, text="Admin")

        self.current_user = "Guest"
        self.build_login_tab()
        self.build_inventory_tab()
        self.build_booking_tab()
        self.build_admin_tab()

    def connect_db(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            if conn.is_connected():
                return conn
            return None
        except Error as exc:
            messagebox.showerror("Database Connection Error", f"{exc}")
            return None

    @staticmethod
    def generate_booking_id():
        letters = "".join(random.choices(string.ascii_uppercase, k=2))
        numbers = "".join(random.choices(string.digits, k=6))
        return f"BK{letters}{numbers}"

    def build_login_tab(self):
        tk.Label(self.login_frame, text="AutoSpec Car System", font=("Segoe UI", 22, "bold")).pack(pady=(30, 20))

        login_card = ttk.Frame(self.login_frame, padding=20)
        login_card.pack(padx=150, pady=20)

        tk.Label(login_card, text="Username", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=8)
        self.username_entry = ttk.Entry(login_card, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(login_card, text="Password", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.password_entry = ttk.Entry(login_card, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=8)

        ttk.Button(login_card, text="Login as Admin", command=self.admin_login).grid(row=2, column=0, columnspan=2, pady=(18, 5), sticky="ew")
        ttk.Button(login_card, text="Continue as Guest", command=self.continue_as_guest).grid(row=3, column=0, columnspan=2, sticky="ew")

        self.login_status = tk.StringVar(value="Ready")
        tk.Label(self.login_frame, textvariable=self.login_status, fg="darkgreen", font=("Segoe UI", 10, "bold")).pack(pady=10)

    def build_inventory_tab(self):
        top = ttk.Frame(self.inventory_frame)
        top.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(top, text="Min Price (INR)", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.min_price = ttk.Entry(top, width=14)
        self.min_price.grid(row=0, column=1, padx=5)

        ttk.Label(top, text="Max Price (INR)", font=("Segoe UI", 10)).grid(row=0, column=2, padx=5, pady=5)
        self.max_price = ttk.Entry(top, width=14)
        self.max_price.grid(row=0, column=3, padx=5)

        ttk.Label(top, text="Fuel", font=("Segoe UI", 10)).grid(row=0, column=4, padx=5, pady=5)
        self.fuel_var = tk.StringVar(value="")
        ttk.Combobox(top, textvariable=self.fuel_var, values=["", "Petrol", "Diesel", "Electric", "Hybrid"], width=12, state="readonly").grid(row=0, column=5, padx=5)

        ttk.Label(top, text="Body Type", font=("Segoe UI", 10)).grid(row=0, column=6, padx=5, pady=5)
        self.body_var = tk.StringVar(value="")
        ttk.Combobox(top, textvariable=self.body_var, values=["", "SUV", "Sedan", "Hatchback", "Coupe", "Luxury"], width=12, state="readonly").grid(row=0, column=7, padx=5)

        ttk.Button(top, text="Search Inventory", command=self.load_inventory).grid(row=0, column=8, padx=10)
        ttk.Button(top, text="View All", command=self.load_inventory).grid(row=0, column=9, padx=10)

        columns = ("Brand", "Model", "Variant", "Price", "Engine", "Power", "Fuel", "Transmission", "Drive")
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=columns, show="headings")
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=130, anchor="center")
        self.inventory_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        scrollbar = ttk.Scrollbar(self.inventory_frame, orient="vertical", command=self.inventory_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)

        self.load_inventory()

    def build_booking_tab(self):
        form = ttk.Frame(self.booking_frame, padding=20)
        form.pack(fill=tk.BOTH, expand=True)

        labels = [
            ("Customer Name", 0), ("Contact", 1), ("Email", 2),
            ("Selected Variant ID", 3), ("Booking Date", 4)
        ]

        self.booking_name = ttk.Entry(form, width=30)
        self.booking_contact = ttk.Entry(form, width=30)
        self.booking_email = ttk.Entry(form, width=30)
        self.booking_variant = ttk.Entry(form, width=30)
        self.booking_date = ttk.Entry(form, width=30)

        entries = [self.booking_name, self.booking_contact, self.booking_email, self.booking_variant, self.booking_date]

        for (text, row) in labels:
            ttk.Label(form, text=text).grid(row=row, column=0, sticky="w", padx=10, pady=8)

        for idx, entry in enumerate(entries):
            entry.grid(row=idx, column=1, padx=10, pady=8, sticky="ew")

        ttk.Button(form, text="Book This Car", command=self.create_booking).grid(row=5, column=0, columnspan=2, pady=20)

        self.booking_status = tk.StringVar(value="Select a car variant ID from inventory and create a booking.")
        ttk.Label(form, textvariable=self.booking_status, wraplength=500, justify="left").grid(row=6, column=0, columnspan=2, sticky="w", padx=10)

        self.bookings_tree = ttk.Treeview(self.booking_frame, columns=("Booking ID", "Customer", "Contact", "Email", "Variant ID", "Date", "Status"), show="headings")
        for col in ("Booking ID", "Customer", "Contact", "Email", "Variant ID", "Date", "Status"):
            self.bookings_tree.heading(col, text=col)
            self.bookings_tree.column(col, width=140, anchor="center")
        self.bookings_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        ttk.Button(self.booking_frame, text="Refresh Bookings", command=self.load_bookings).pack(pady=(0, 10))
        self.load_bookings()

    def build_admin_tab(self):
        ttk.Label(self.admin_frame, text="Admin Controls", font=("Segoe UI", 18, "bold")).pack(pady=(20, 10))

        admin_controls = ttk.Frame(self.admin_frame)
        admin_controls.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Label(admin_controls, text="Brand", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.admin_brand = ttk.Entry(admin_controls, width=25)
        self.admin_brand.grid(row=0, column=1, padx=10, pady=8)

        ttk.Label(admin_controls, text="Model", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.admin_model = ttk.Entry(admin_controls, width=25)
        self.admin_model.grid(row=1, column=1, padx=10, pady=8)

        ttk.Label(admin_controls, text="Variant", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=8)
        self.admin_variant = ttk.Entry(admin_controls, width=25)
        self.admin_variant.grid(row=2, column=1, padx=10, pady=8)

        ttk.Label(admin_controls, text="Price (INR)", font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", padx=10, pady=8)
        self.admin_price = ttk.Entry(admin_controls, width=25)
        self.admin_price.grid(row=3, column=1, padx=10, pady=8)

        ttk.Button(admin_controls, text="Add Sample Car", command=self.add_sample_car).grid(row=4, column=0, columnspan=2, pady=15, sticky="ew")
        ttk.Button(admin_controls, text="Reset Database", command=self.reset_database).grid(row=5, column=0, columnspan=2, sticky="ew")

        self.admin_status = tk.StringVar(value="Admin mode is available after login")
        ttk.Label(admin_controls, textvariable=self.admin_status, foreground="darkblue", justify="left").grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=10)

    def admin_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "admin" and password == "Verstappen@1":
            self.current_user = "Admin"
            self.login_status.set("Admin login successful")
            self.admin_status.set("Admin access granted")
            self.notebook.select(3)
        else:
            self.login_status.set("Incorrect admin username/password")
            messagebox.showerror("Access Denied", "Please use admin / Verstappen@1")

    def continue_as_guest(self):
        self.current_user = "Guest"
        self.login_status.set("Guest mode enabled")
        self.notebook.select(1)

    def load_inventory(self):
        query = """
            SELECT b.brand_name, m.model_name, v.variant_name, v.price_inr, v.engine,
                   v.power_bhp, v.fuel_type, v.transmission, v.drivetrain
            FROM variants v
            JOIN models m ON v.model_id = m.model_id
            JOIN brands b ON m.brand_id = b.brand_id
        """

        filters = []
        values = []

        min_price = self.min_price.get().strip()
        max_price = self.max_price.get().strip()
        fuel = self.fuel_var.get().strip()
        body = self.body_var.get().strip()

        if min_price:
            filters.append("v.price_inr >= %s")
            values.append(float(min_price))
        if max_price:
            filters.append("v.price_inr <= %s")
            values.append(float(max_price))
        if fuel:
            filters.append("v.fuel_type LIKE %s")
            values.append(f"%{fuel}%")
        if body:
            filters.append("m.body_type LIKE %s")
            values.append(f"%{body}%")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " ORDER BY b.brand_name, m.model_name, v.variant_name"

        conn = self.connect_db()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(query, values)
            rows = cursor.fetchall()
        finally:
            conn.close()

        for row in self.inventory_tree.get_children():
            self.inventory_tree.delete(row)

        if not rows:
            self.booking_status.set("No inventory found for the current filter.")
            return

        for row in rows:
            self.inventory_tree.insert("", tk.END, values=row)

        self.booking_status.set(f"Loaded {len(rows)} car options. Use the variant name/ID from the table to book a car.")

    def create_booking(self):
        customer_name = self.booking_name.get().strip()
        contact = self.booking_contact.get().strip()
        email = self.booking_email.get().strip()
        variant_id = self.booking_variant.get().strip()
        date = self.booking_date.get().strip() or "2026-10-08"

        if not all([customer_name, contact, email, variant_id]):
            messagebox.showwarning("Missing Details", "Please fill in all booking fields.")
            return

        conn = self.connect_db()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT variant_id FROM variants WHERE variant_id = %s", (variant_id,))
            if cursor.fetchone() is None:
                messagebox.showwarning("Invalid Variant", "The selected variant ID does not exist.")
                return

            booking_id = self.generate_booking_id()
            cursor.execute(
                """
                INSERT INTO bookings (booking_id, variant_id, customer_name, customer_contact,
                                     customer_email, booking_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Active')
                """,
                (booking_id, variant_id, customer_name, contact, email, date),
            )
            conn.commit()
            self.booking_status.set(f"Booking created successfully. Booking ID: {booking_id}")
            self.load_bookings()
        except Error as exc:
            messagebox.showerror("Booking Error", f"{exc}")
        finally:
            conn.close()

    def load_bookings(self):
        conn = self.connect_db()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT booking_id, customer_name, customer_contact, customer_email,
                       variant_id, booking_date, status
                FROM bookings
                ORDER BY booking_date DESC
                """
            )
            rows = cursor.fetchall()
        finally:
            conn.close()

        for row in self.bookings_tree.get_children():
            self.bookings_tree.delete(row)

        if rows:
            for row in rows:
                self.bookings_tree.insert("", tk.END, values=row)

    def add_sample_car(self):
        brand = self.admin_brand.get().strip()
        model = self.admin_model.get().strip()
        variant = self.admin_variant.get().strip()
        price = self.admin_price.get().strip()

        if not all([brand, model, variant, price]):
            self.admin_status.set("Please fill in all admin fields")
            return

        conn = self.connect_db()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT brand_id FROM brands WHERE brand_name = %s LIMIT 1", (brand,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute(
                    "INSERT INTO brands (brand_name, country_of_origin, year_founded) VALUES (%s, %s, %s)",
                    (brand, "India", 2024),
                )
                conn.commit()
                brand_id = cursor.lastrowid
            else:
                brand_id = result[0]

            cursor.execute(
                "SELECT model_id FROM models WHERE model_name = %s AND brand_id = %s LIMIT 1",
                (model, brand_id),
            )
            result = cursor.fetchone()
            if result is None:
                cursor.execute(
                    "INSERT INTO models (brand_id, model_name, body_type, category) VALUES (%s, %s, %s, %s)",
                    (brand_id, model, "SUV", "Premium"),
                )
                conn.commit()
                model_id = cursor.lastrowid
            else:
                model_id = result[0]

            cursor.execute(
                "INSERT INTO variants (model_id, variant_name, price_inr, engine, power_bhp, torque_nm, top_speed_kmh, acceleration_0_100, transmission, drivetrain, fuel_type, mileage_range, seating_capacity, safety_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (model_id, variant, float(price), "2.0L Turbo", 220, 420, 210, 7.2, "Automatic", "AWD", "Petrol", 18, 5, "5 Star"),
            )
            conn.commit()
            self.admin_status.set(f"Sample car '{brand} {model} {variant}' added successfully.")
            self.load_inventory()
        except Error as exc:
            self.admin_status.set(f"Error adding car: {exc}")
            messagebox.showerror("Admin Error", str(exc))
        finally:
            conn.close()

    def reset_database(self):
        confirm = messagebox.askyesno("Reset Database", "This will reset the sample data. Continue?")
        if not confirm:
            return

        conn = self.connect_db()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings")
            cursor.execute("DELETE FROM features")
            cursor.execute("DELETE FROM colors")
            cursor.execute("DELETE FROM variants")
            cursor.execute("DELETE FROM models")
            cursor.execute("DELETE FROM brands")
            conn.commit()
            self.admin_status.set("Database reset successfully.")
            self.load_inventory()
            self.load_bookings()
        except Error as exc:
            messagebox.showerror("Reset Error", str(exc))
        finally:
            conn.close()


if __name__ == "__main__":
    app = CarDealerInterface()
    app.mainloop()
