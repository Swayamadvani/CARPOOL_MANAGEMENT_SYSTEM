#Carpool Management System 🚘

A Python Tkinter + MySQL–based application to manage drivers, rides, users, and automatic seat allocation using stored procedures and triggers.

⸻

Overview

This project implements a smart carpool management system that allows:
	•	Adding users and automatically assigning them to rides
	•	Adding rides with driver details
	•	Viewing all rides, users, and grouped summaries
	•	Removing users or rides
	•	Auto-updating seat occupancy
	•	A complete GUI built using Tkinter
	•	A backend built using MySQL stored procedures for clean logic

This system behaves similar to a real-world carpool booking platform.

⸻

 Tech Stack

Frontend / Application
	•	Python
	•	Tkinter (GUI)
	•	ttk TreeView for tables

Backend
	•	MySQL
	•	Stored Procedures
	•	Constraints & Foreign Keys
	•	Cascading rules

⸻

📂 Folder Structure

Carpool-Management-System/
- main.py
- database/
  - schema.sql
- README.md
- requirements.txt


🗄 Database Schema

The system uses 4 main tables:
	1.	Drivers
	2.	Rides
	3.	Users
	4.	Payments (optional)

The SQL includes:
	•	DDL commands
	•	Stored procedures:
	•	AddUserAutoRide
	•	AddRide
	•	RemoveUser
	•	RemoveRide
	•	Cascading relationships
	•	Auto seat handling logic

The full SQL is in:
👉 database/schema.sql

⸻

 Features

✔ Add User
	•	User is automatically assigned to a ride
	•	Stored Procedure checks seat availability
	•	Seat count updates automatically

✔ Add Ride
	•	Add driver (auto-created if not existing)
	•	Add ride with seat capacity

✔ View Details
	•	View all users
	•	View all rides
	•	View grouped summaries with:
	•	Users in ride
	•	Total users
	•	Seats
	•	Occupied seats

✔ Remove User
	•	Automatically decreases seat count

✔ Remove Ride
	•	Auto-removes linked users (CASCADE)

⸻

🖥 Running the Application

Step 1 — Install dependencies

pip install -r requirements.txt

Step 2 — Setup MySQL database
	1.	Open MySQL Workbench or terminal
	2.	Run the SQL file:

SOURCE database/schema.sql;

Step 3 — Update MySQL credentials

Inside main.py, update:

host="localhost"
user="root"
password="YOUR_MYSQL_PASSWORD"

Step 4 — Run the GUI

python main.py


⸻
GUI Features

The application contains 4 tabs:

1️⃣ Add User
	•	Enter user info
	•	Auto-assignment to ride
	•	Table shows current users

2️⃣ Manage Rides
	•	Add new ride
	•	Add driver
	•	View rides table

3️⃣ Remove
	•	Remove user by ID
	•	Remove ride by ID

4️⃣ Summary
	•	Shows ride-wise grouping
	•	Names of all users assigned
	•	Total users & seat status

⸻

🎯 Highlights
	•	Real-world relational DB design
	•	Auto seat management
	•	Stored procedure–based logic
	•	User-friendly GUI
	•	Clean and scalable project

⸻

👨‍💻 Author

Swayam Advani
B.Tech AIML
PES University

⸻

📄 License

This project is open-source and free to use for academic or learning purposes.
