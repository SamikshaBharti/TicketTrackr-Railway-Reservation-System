import mysql.connector
from getpass import getpass
import hashlib
import re
import logging

logging.basicConfig(level = logging.INFO ,format = '%(asctime)s - %(levelname)s - %(message)s')

#MySQL connection parameter
username = 'user_name'   # Replace with actual MySQL username
password = 'password'  # This will ask for a password when you run
host = 'localhost'           # Use 'localhost' if MySQL is on your machine
database = 'railway_reservation'

try:
    cnx = mysql.connector.connect(
        user = username,
        password = password,
        host = host,
        database = database
    )

    cursor = cnx.cursor()
    logging.info("Connected to the database successfully.")

except mysql.connector.Error as err:
    logging.error(f"Error connecting to the database: {err}")
    exit(1)

# Function to hash passwords using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


#validate email function
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


#validate data input function
def validate_date(date_str):
    try:
        return bool(re.match(r'\d{4}-\d{2}-\d{2}',date_str))
    except ValueError:
        return False
    
#function to create tables in database
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

def seed_users():
    users = [
        ('sam', 'password123', 'sam@example.com'),
        ('ruchi', 'securepass', 'ruchi@example.com'),
        ('keval', 'mypassword', 'keval@example.com'),
        ('dev', 'pass1234', 'dev@example.com'),
        ('payal', 'evepass', 'payal@example.com')
    ]
    for username, password, email in users:
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, hash_password(password), email)
            )
        except mysql.connector.Error:
            pass
    cnx.commit()
    logging.info("Sample users inserted.")

def seed_employees():
    employees = [
        ('emp1', 'emp1pass', 'emp1@example.com'),
        ('emp2', 'emp2pass', 'emp2@example.com'),
        ('emp3', 'emp3pass', 'emp3@example.com')
    ]
    for username, password, email in employees:
        try:
            cursor.execute(
                "INSERT INTO employees (username, password, email) VALUES (%s, %s, %s)",
                (username, hash_password(password), email)
            )
        except mysql.connector.Error:
            pass
    cnx.commit()
    logging.info("Sample employees inserted.")

def seed_trains():
    try:
        cursor.execute("DELETE FROM trains")  # clear the table
        cnx.commit()
    except mysql.connector.Error as err:
        logging.error(f"Error clearing trains: {err}")
        cnx.rollback()

    trains = [
        (201, 'Gomti Express', 'Lucknow', 'New Delhi', '06:00:00'),
        (202, 'Krishak Express', 'Varanasi', 'Lucknow', '07:15:00'),
        (203, 'Shatabdi Express', 'Lucknow', 'Kanpur', '08:30:00'),
        (204, 'Lucknow Mail', 'Lucknow', 'Anand Vihar', '22:00:00'),
        (205, 'Avadh Express', 'Mumbai', 'Lucknow', '15:45:00'),
        (206, 'Chandigarh Express', 'Chandigarh', 'Delhi', '11:00:00'),
        (207, 'Lucknow Intercity', 'Lucknow', 'Chandigarh', '05:30:00'),
        (208, 'Ganga Sutlej Expsress', 'Chandigarh', 'Lucknow', '04:45:00'),
        (209, 'Chandigarh Jan Shatabdi', 'Chandigarh', 'Amritsar', '07:10:00'),
        (210, 'Shramjeevi Express', 'Lucknow', 'Rajgir', '13:40:00')
    ]

    for train in trains:
        try:
            cursor.execute("""
                INSERT INTO trains (train_number, train_name, source_station, destination_station, schedule)
                VALUES (%s, %s, %s, %s, %s)
            """, train)
        except mysql.connector.Error as err:
            logging.error(f"Error inserting train {train[1]}: {err}")
    cnx.commit()
    logging.info("Updated train list inserted.")


def seed_bookings():
    bookings = [
        (1, 1, '2025-06-01'),
        (2, 3, '2025-06-02'),
        (3, 2, '2025-06-05'),
        (4, 5, '2025-06-10'),
        (5, 4, '2025-06-15'),
        (1, 6, '2025-07-01'),
        (2, 7, '2025-07-04'),
        (3, 8, '2025-07-07'),
        (4, 9, '2025-07-09'),
        (5, 10, '2025-07-12')
    ]
    for user_id, train_id, booking_date in bookings:
        try:
            cursor.execute(
                "INSERT INTO bookings (user_id, train_id, booking_date) VALUES (%s, %s, %s)",
                (user_id, train_id, booking_date)
            )
        except mysql.connector.Error:
            pass
    cnx.commit()
    logging.info("Sample bookings inserted.")

# Main function to interact with the railway reservation system
def main():
    create_table()
    

    # Seed data after tables creation
    seed_users()
    seed_employees()
    seed_trains()
    seed_bookings()



    while True:
        print("1. User Login")
        print("2. User Signup")
        print("3. Employee Login")
        print("4. Employee Signup")
        print("5. View Train Schedule")
        print("6. Book a Ticket")
        print("7. Cancel a Ticket")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            user = login_user(username, password)
            if user:
                print("Login successful!")
            else:
                print("Invalid username or password.")
        elif choice == "2":
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            email = input("Enter email: ")
            signup_user(username, password, email)
        elif choice == "3":
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            employee = login_employee(username, password)
            if employee:
                print("Login successful!")
            else:
                print("Invalid username or password.")
        elif choice == "4":
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            email = input("Enter email: ")
            signup_employee(username, password, email)
        elif choice == "5":
            view_train_schedule()
        elif choice == "6":
            user_id = int(input("Enter user ID: "))
            train_id = int(input("Enter train ID: "))
            booking_date = input("Enter booking date (YYYY-MM-DD): ")
            book_ticket(user_id, train_id, booking_date)
        elif choice == "7":
            booking_id = int(input("Enter booking ID: "))
            cancel_ticket(booking_id)
        elif choice == "8":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
 

