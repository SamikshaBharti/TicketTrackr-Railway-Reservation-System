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
