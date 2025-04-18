

class InitializeDatabase:
    def __init__(self, cursor):

        self.cursor = cursor

        self.initialize_db()

    def initialize_db(self):

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS guests(
        guest_id VARCHAR(12) NOT NULL,
        name VARCHAR(255) NOT NULL, 
        sex ENUM('male', 'female', 'others', 'prefer not to say') NOT NULL, 
        home_address VARCHAR(255) NOT NULL, 
        email_address VARCHAR(255) NOT NULL, 
        phone_number VARCHAR(13) NOT NULL, 
        birth_date DATE NOT NULL, 
        government_id VARCHAR(255) NOT NULL, 
        last_visit_date DATE, 
        visit_count SMALLINT NOT NULL,
        PRIMARY KEY (guest_id),         
        CONSTRAINT UC_email_address UNIQUE (email_address),
        CONSTRAINT UC_phone_number UNIQUE (phone_number),
        CONSTRAINT UC_government_id UNIQUE (government_id)
        )
        """)

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS rooms(
        room_number VARCHAR(9) NOT NULL,
        room_type VARCHAR(25) NOT NULL, 
        price INT NOT NULL, 
        availability_status ENUM('available', 'reserved', 'occupied') NOT NULL, 
        capacity SMALLINT NOT NULL, 
        PRIMARY KEY (room_number)
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS reservedRooms(
        reservation_id VARCHAR(13) NOT NULL,
        reservation_date DATETIME NOT NULL, 
        check_in_date DATETIME NOT NULL, 
        check_out_date DATETIME NOT NULL, 
        payment_status ENUM('not paid', 'partially paid', 'fully paid') NOT NULL, 
        guest_id VARCHAR(12) NOT NULL, 
        room_number VARCHAR(9) NOT NULL, 
        FOREIGN KEY(guest_id) REFERENCES Guests(guest_id),
        FOREIGN KEY(room_number) REFERENCES Rooms(room_number), 
        PRIMARY KEY (reservation_id),
        CONSTRAINT check_in_date_limit CHECK (check_in_date <= check_out_date)
        )""")

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS bookedRooms(
        booking_id VARCHAR(10) NOT NULL,
        check_in_status ENUM('checked in', 'checked out') NOT NULL, 
        check_in_date DATETIME NOT NULL, 
        check_out_date DATETIME NOT NULL, 
        guest_id VARCHAR(12) NOT NULL, 
        room_number VARCHAR(9) NOT NULL, 
        FOREIGN KEY(guest_id) REFERENCES guests(guest_id),
        FOREIGN KEY(room_number) REFERENCES rooms(room_number), 
        PRIMARY KEY (room_number)
        )""")

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS paidRooms(
        payment_id VARCHAR(12) NOT NULL,
        payment_type VARCHAR(20) NOT NULL, 
        amount INT NOT NULL, 
        transaction_date DATE NOT NULL, 
        guest_id VARCHAR(10) NOT NULL, 
        room_number VARCHAR(9) NOT NULL, 
        FOREIGN KEY(guest_id) REFERENCES guests(guest_id),
        FOREIGN KEY(room_number) REFERENCES rooms(room_number),
        PRIMARY KEY (payment_id)
        )
        """)

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS services(
        service_id VARCHAR(11) NOT NULL,
        service_name VARCHAR(20) NOT NULL, 
        rate INT NOT NULL, 
        PRIMARY KEY (service_id),
        CONSTRAINT UC_service_name UNIQUE (service_name)
        )
        """)

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS availedServices(
        avail_id VARCHAR(12) NOT NULL,
        avail_date DATE NOT NULL, 
        guest_id VARCHAR(12) NOT NULL, 
        service_id VARCHAR(11) NOT NULL, 
        FOREIGN KEY(guest_id) REFERENCES guests(guest_id),
        FOREIGN KEY(service_id) REFERENCES services(service_id),
        PRIMARY KEY (avail_id)
        )
        """)
