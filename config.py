import mysql.connector
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_db():
    try:
        cnx = mysql.connector.connect(
            user='user_name',
            password='password',
            host='localhost',
            database='railway_reservation'
        )
        logging.info("Connected to the database successfully.")
        return cnx, cnx.cursor()
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to the database: {err}")
        exit(1)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
