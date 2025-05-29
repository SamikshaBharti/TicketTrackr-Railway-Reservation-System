import mysql.connector
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Establish database connection
try:
    cnx = mysql.connector.connect(
        host="localhost",
        user="yourusername",       # <-- Replace with your DB username
        password="yourpassword",   # <-- Replace with your DB password
        database="yourdatabase"    # <-- Replace with your DB name
    )
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    logging.error(f"Database connection error: {err}")
    exit(1)

# Seed users table
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
        except mysql.connector.Error as err:
            logging.warning(f"Skipping user {username}: {err}")
    cnx.commit()
    logging.info("Sample users inserted.")

# Seed employees table
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
        except mysql.connector.Error as err:
            logging.warning(f"Skipping employee {username}: {err}")
    cnx.commit()
    logging.info("Sample employees inserted.")

# Seed trains table
def seed_trains():
    try:
        cursor.execute("DELETE FROM trains")  # Clear existing data
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
        (208, 'Ganga Sutlej Express', 'Chandigarh', 'Lucknow', '04:45:00'),
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

# Seed bookings table
def seed_bookings():
    bookings = [
        (1, 201, '2025-06-01'),
        (2, 203, '2025-06-02'),
        (3, 202, '2025-06-05'),
        (4, 205, '2025-06-10'),
        (5, 204, '2025-06-15'),
        (1, 206, '2025-07-01'),
        (2, 207, '2025-07-04'),
        (3, 208, '2025-07-07'),
        (4, 209, '2025-07-09'),
        (5, 210, '2025-07-12')
    ]
    for user_id, train_number, booking_date in bookings:
        try:
            cursor.execute(
                "INSERT INTO bookings (user_id, train_id, booking_date) VALUES (%s, %s, %s)",
                (user_id, train_number, booking_date)
            )
        except mysql.connector.Error as err:
            logging.warning(f"Skipping booking for user {user_id}: {err}")
    cnx.commit()
    logging.info("Sample bookings inserted.")

# Main block to call all seed functions
if __name__ == "__main__":
    seed_users()
    seed_employees()
    seed_trains()
    seed_bookings()
    cursor.close()
    cnx.close()
    logging.info("Database seeding completed.")
