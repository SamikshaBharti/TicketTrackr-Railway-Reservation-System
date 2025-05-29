from config import hash_password
import re
import mysql.connector
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


#validate data input function
def validate_date(date_str):
    try:
        return bool(re.match(r'\d{4}-\d{2}-\d{2}',date_str))
    except ValueError:
        return False
    
#function to create tables in a database
def create_table():
    try:
        cursor.execute("""
                Create table if not exists users(
                       id int auto_increment,
                       username varchar(50) unique,
                       password varchar(100),
                       email varchar(100),
                       primary key(id)
                    );
                """)
        cursor.execute("""
                Create table if not exists employees(
                       id int auto_increment,
                       username varchar(50) unique,
                       password varchar(100),
                       email varchar(100),
                       primary key(id)
                    );
                """)
        cursor.execute("""
                Create table if not exists trains(
                       id int auto_increment,
                       train_number int unique,
                       train_name varchar(100),
                       source_station varchar(50),
                       destination_station varchar(50),
                       schedule time,
                       primary key(id)
                    );
                """)
        cursor.execute("""
                Create table if not exists bookings(
                       id int auto_increment,
                        user_id int,
                        train_id int,
                        booking_date DATE,
                        primary key (id),
                        foreign key (user_id) references users(id),
                        foreign key (train_id) references trains(id)
                    );
                """)
        cnx.commit()
        logging.info("Tables created successfully.")
    except mysql.connector.Error as err:
        logging.error(f"Error creating tables: {err}")
        cnx.rollback()

def login_employee(username, password):
    try:
        cursor.execute("SELECT * FROM employees WHERE username = %s AND password = %s", (username, hash_password(password)))
        employee = cursor.fetchone()
        return employee
    except mysql.connector.Error as err:
        logging.error(f"Error during employee login: {err}")
        return None


# Function to signup for employees
def signup_employee(username, password, email):
    if not validate_email(email):
        print("Invalid email format.")
        return
    try:
        cursor.execute("INSERT INTO employees (username, password, email) VALUES (%s, %s, %s)", (username, hash_password(password), email))
        cnx.commit()
        logging.info("Employee signup successful.")
    except mysql.connector.Error as err:
        logging.error(f"Error during employee signup: {err}")
        cnx.rollback()


# Function to view train schedule
def view_train_schedule():
    try:
        cursor.execute("SELECT * FROM trains")
        trains = cursor.fetchall()
        for train in trains:
            print(f"Train Number: {train[1]}, Train Name: {train[2]}, Source: {train[3]}, Destination: {train[4]}, Schedule: {train[5]}")
    except mysql.connector.Error as err:
        logging.error(f"Error viewing train schedule: {err}")


# Function to book a ticket
def book_ticket(user_id, train_id, booking_date):
    if not validate_date(booking_date):
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    try:
        cursor.execute("INSERT INTO bookings (user_id, train_id, booking_date) VALUES (%s, %s, %s)", (user_id, train_id, booking_date))
        cnx.commit()
        logging.info("Ticket booked successfully.")
    except mysql.connector.Error as err:
        logging.error(f"Error booking ticket: {err}")
        cnx.rollback()


# Function to cancel a ticket
def cancel_ticket(booking_id):
    try:
        cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        cnx.commit()
        logging.info("Ticket cancelled successfully.")
    except mysql.connector.Error as err:
        logging.error(f"Error cancelling ticket: {err}")
        cnx.rollback()
def login_user(username, password):
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hash_password(password)))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        logging.error(f"Error during user login: {err}")
        return None

def signup_user(username, password, email):
    if not validate_email(email):
        print("Invalid email format.")
        return
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, hash_password(password), email))
        cnx.commit()
        logging.info("User signup successful.")
    except mysql.connector.Error as err:
        logging.error(f"Error during user signup: {err}")
        cnx.rollback()
