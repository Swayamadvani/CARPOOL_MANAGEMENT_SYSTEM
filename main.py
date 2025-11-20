import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------------- Database Connection ----------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",  # 🔹 replace with your MySQL root password
        database="CarpoolDB"
    )

# ---------------- Core Functions ----------------
def add_user():
    name = entry_name.get()
    age = entry_age.get()
    pickup = entry_pickup.get()
    drop = entry_drop.get()

    if not (name and age and pickup and drop):
        messagebox.showerror("Error", "Please fill all fields before adding a user.")
        return

    try:
        db = connect_db()
        cur = db.cursor()

        # Call stored procedure (SQL handles ride logic)
        cur.callproc('AddUserAutoRide', (name, int(age), pickup, drop))
        db.commit()

        messagebox.showinfo("Success", f"User '{name}' added successfully and assigned to a ride!")

        # Refresh UI tables
        clear_user_entries()
        view_users()
        view_rides()

    except mysql.connector.Error as e:
        # SQLSTATE 45000 = custom SIGNAL error from stored procedure
        if e.errno == 1644 or "No available rides" in str(e):
            messagebox.showwarning("No Rides", "No rides available for this route or all rides are full.")
        else:
            messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        db.close()


def add_ride():
    pickup = entry_ride_pickup.get()
    drop = entry_ride_drop.get()
    driver = entry_driver.get()
    seats = entry_seats.get()

    if not (pickup and drop and driver and seats):
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        db = connect_db()
        cur = db.cursor()

        # Create driver if not exists
        cur.execute("SELECT d_id FROM Driver WHERE driver_name = %s", (driver,))
        driver_row = cur.fetchone()
        if driver_row:
            d_id = driver_row[0]
        else:
            cur.execute("INSERT INTO Driver (driver_name) VALUES (%s)", (driver,))
            db.commit()
            d_id = cur.lastrowid

        cur.execute("""
            INSERT INTO Ride (pickup, drop_loc, d_id, no_of_seats, occupied)
            VALUES (%s, %s, %s, %s, 0)
        """, (pickup, drop, d_id, seats))
        db.commit()
        messagebox.showinfo("Success", f"Ride from {pickup} to {drop} added!")
        clear_ride_entries()
        view_rides()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        db.close()

def remove_user():
    uid = entry_remove_user.get()
    if not uid:
        messagebox.showerror("Error", "Enter User ID to remove")
        return
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("DELETE FROM User WHERE user_id = %s", (uid,))
        db.commit()
        messagebox.showinfo("Removed", f"User {uid} removed successfully!")
        entry_remove_user.delete(0, tk.END)
        view_users()
        view_rides()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        db.close()

def remove_ride():
    rid = entry_remove_ride.get()
    if not rid:
        messagebox.showerror("Error", "Enter Ride ID to remove")
        return
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("DELETE FROM Ride WHERE ride_id = %s", (rid,))
        db.commit()
        messagebox.showinfo("Removed", f"Ride {rid} removed successfully!")
        entry_remove_ride.delete(0, tk.END)
        view_rides()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        db.close()

def view_users():
    for i in tree_users.get_children():
        tree_users.delete(i)
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT user_id, name, age, pickup, drop_loc FROM User")
        for row in cur.fetchall():
            tree_users.insert('', 'end', values=row)
    finally:
        db.close()

def view_rides():
    for i in tree_rides.get_children():
        tree_rides.delete(i)
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("""
            SELECT R.ride_id, R.pickup, R.drop_loc, D.driver_name, 
                   R.no_of_seats, R.occupied
            FROM Ride R JOIN Driver D ON R.d_id = D.d_id
        """)
        for row in cur.fetchall():
            tree_rides.insert('', 'end', values=row)
    finally:
        db.close()

def view_summary():
    for i in tree_summary.get_children():
        tree_summary.delete(i)
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("""
            SELECT R.ride_id, R.pickup, R.drop_loc,
                   GROUP_CONCAT(U.name SEPARATOR ', ') AS users,
                   COUNT(U.user_id) AS total_users,
                   R.no_of_seats, R.occupied
            FROM Ride R
            LEFT JOIN Ride_Assignment A ON R.ride_id = A.ride_id
            LEFT JOIN User U ON A.user_id = U.user_id
            GROUP BY R.ride_id;
        """)
        for row in cur.fetchall():
            tree_summary.insert('', 'end', values=row)
    finally:
        db.close()

# ---------------- Utility ----------------
def clear_user_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_pickup.delete(0, tk.END)
    entry_drop.delete(0, tk.END)

def clear_ride_entries():
    entry_ride_pickup.delete(0, tk.END)
    entry_ride_drop.delete(0, tk.END)
    entry_driver.delete(0, tk.END)
    entry_seats.delete(0, tk.END)

# ---------------- GUI Layout ----------------
root = tk.Tk() 
root.title("Carpool Management System")
root.geometry("950x700")
root.configure(bg="#e8f0fe")

style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 10))
style.configure("TLabel", font=("Helvetica", 11))
style.configure("TButton", font=("Helvetica", 11, "bold"), padding=6)

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

# --------------- Tab 1: Add User -----------------
tab_user = ttk.Frame(tabs)
tabs.add(tab_user, text="Add User")

ttk.Label(tab_user, text="Name:").grid(row=0, column=0, padx=10, pady=8)
entry_name = ttk.Entry(tab_user); entry_name.grid(row=0, column=1, pady=8)

ttk.Label(tab_user, text="Age:").grid(row=1, column=0)
entry_age = ttk.Entry(tab_user); entry_age.grid(row=1, column=1, pady=8)

ttk.Label(tab_user, text="Pickup:").grid(row=2, column=0)
entry_pickup = ttk.Entry(tab_user); entry_pickup.grid(row=2, column=1, pady=8)

ttk.Label(tab_user, text="Drop:").grid(row=3, column=0)
entry_drop = ttk.Entry(tab_user); entry_drop.grid(row=3, column=1, pady=8)

ttk.Button(tab_user, text="Add User", command=add_user).grid(row=4, column=0, columnspan=2, pady=10)

tree_users = ttk.Treeview(tab_user, columns=("ID","Name","Age","Pickup","Drop"), show="headings")
for col in ("ID","Name","Age","Pickup","Drop"):
    tree_users.heading(col, text=col)
tree_users.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
ttk.Button(tab_user, text="Refresh", command=view_users).grid(row=6, column=0, columnspan=2)

# --------------- Tab 2: Manage Rides -----------------
tab_rides = ttk.Frame(tabs)
tabs.add(tab_rides, text="Manage Rides")

ttk.Label(tab_rides, text="Pickup:").grid(row=0, column=0)
entry_ride_pickup = ttk.Entry(tab_rides); entry_ride_pickup.grid(row=0, column=1, pady=8)

ttk.Label(tab_rides, text="Drop:").grid(row=1, column=0)
entry_ride_drop = ttk.Entry(tab_rides); entry_ride_drop.grid(row=1, column=1, pady=8)

ttk.Label(tab_rides, text="Driver Name:").grid(row=2, column=0)
entry_driver = ttk.Entry(tab_rides); entry_driver.grid(row=2, column=1, pady=8)

ttk.Label(tab_rides, text="No. of Seats:").grid(row=3, column=0)
entry_seats = ttk.Entry(tab_rides); entry_seats.grid(row=3, column=1, pady=8)

ttk.Button(tab_rides, text="Add Ride", command=add_ride).grid(row=4, column=0, columnspan=2, pady=10)

tree_rides = ttk.Treeview(tab_rides, columns=("RideID","Pickup","Drop","Driver","Seats","Occupied"), show="headings")
for col in ("RideID","Pickup","Drop","Driver","Seats","Occupied"):
    tree_rides.heading(col, text=col)
tree_rides.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
ttk.Button(tab_rides, text="Refresh", command=view_rides).grid(row=6, column=0, columnspan=2)

# --------------- Tab 3: Remove -----------------
tab_remove = ttk.Frame(tabs)
tabs.add(tab_remove, text="Remove")

ttk.Label(tab_remove, text="User ID:").grid(row=0, column=0, padx=10, pady=8)
entry_remove_user = ttk.Entry(tab_remove); entry_remove_user.grid(row=0, column=1, pady=8)
ttk.Button(tab_remove, text="Remove User", command=remove_user).grid(row=1, column=0, columnspan=2, pady=10)

ttk.Label(tab_remove, text="Ride ID:").grid(row=2, column=0, padx=10, pady=8)
entry_remove_ride = ttk.Entry(tab_remove); entry_remove_ride.grid(row=2, column=1, pady=8)
ttk.Button(tab_remove, text="Remove Ride", command=remove_ride).grid(row=3, column=0, columnspan=2, pady=10)

# --------------- Tab 4: Summary -----------------
tab_summary = ttk.Frame(tabs)
tabs.add(tab_summary, text="Group Summary")

tree_summary = ttk.Treeview(tab_summary,
    columns=("RideID","Pickup","Drop","Users","TotalUsers","Seats","Occupied"),
    show="headings", height=15)
for col in ("RideID","Pickup","Drop","Users","TotalUsers","Seats","Occupied"):
    tree_summary.heading(col, text=col)
tree_summary.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

ttk.Button(tab_summary, text="Refresh Summary", command=view_summary).grid(row=1, column=0, columnspan=2, pady=10)

# Start the GUI
root.mainloop()
