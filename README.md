# TicketTrackr-Railway-Reservation-System
A Python desktop application for booking train tickets and scheduling. Developed with Tkinter GUI and MySQL database, it supports secure employee and user login, ticket booking, cancellation, and real-time display of train schedules.

![Screenshot 2025-05-29 211209](https://github.com/user-attachments/assets/e64df2b3-539b-4997-beaf-3d2bae8a9195)


config.py
- This file has the basic setup needed to connect to the MySQL database, like the hostname, username, password, and database name. It acts like a central place where the database connection details are stored, so we can easily use them in other files without repeating the same code..

function.py
-This is the file where all the main work happens in the background. It has the code for signing up and logging in users, booking and cancelling tickets, checking train details, and allowing employees to add or delete trains. It also has useful tools to check if inputs are correct and to work with the database. This file keeps the core logic separate from the design part, which makes the system easier to manage and update.

gui.py
Using Tkinter, this file builds the graphical interface (the windows, buttons, and forms). It provides login screens for users and employees, a registration page, and ticket booking screens. It helps users interact with the system in a simple and visual way, and it connects all the buttons and forms to the logic written in function.py.

railway_system.py
This is the main file that connects everything. When you run it, it starts the whole system. It checks if the database tables are created, connects the logic, GUI, and database, and finally opens the main application window. This is the file you need to run to use the project.

schema.py
This file creates all the necessary tables in the database, like the tables for users, trains, employees, and bookings. It sets the structure so that the data is stored properly and makes sure all the connections between the tables (like primary keys and foreign keys) are correct.

seed_data.py
This file fills the database with some sample data like example users, employees, and trains with routes and timings. It helps you test the project quickly without having to enter everything manually. It's useful when you're showing a demo or just checking how the system works.



