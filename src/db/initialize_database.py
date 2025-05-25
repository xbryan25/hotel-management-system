

class InitializeDatabase:
    def __init__(self, cursor):

        self.cursor = cursor

        self.initialize_db()

    def initialize_db(self):

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS guests(
        guest_id VARCHAR(12) NOT NULL,
        name VARCHAR(255) NOT NULL, 
        gender ENUM('Male', 'Female', 'Others', 'Prefer not to say') NOT NULL, 
        home_address VARCHAR(255) NOT NULL, 
        email_address VARCHAR(255) NOT NULL, 
        phone_number VARCHAR(11) NOT NULL, 
        birth_date DATE NOT NULL, 
        government_id VARCHAR(255), 
        last_visit_date DATE, 
        visit_count SMALLINT NOT NULL,
        
        PRIMARY KEY (guest_id),
        
        UNIQUE KEY UC_government_id (government_id),
        UNIQUE KEY UC_name (name)
        )
        """)

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS rooms(
        room_id varchar(11) NOT NULL,
        room_number VARCHAR(6) NOT NULL,
        room_type VARCHAR(25) NOT NULL,
        daily_rate INT NOT NULL, 
        availability_status ENUM('Available', 'Reserved', 'Occupied', 'Maintenance', 'Not Available') NOT NULL, 
        capacity SMALLINT NOT NULL,
        is_active TINYINT NOT NULL,
        image_file_name VARCHAR(200), 
        
        PRIMARY KEY (room_id)
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS reservedrooms(
        reservation_id VARCHAR(14) NOT NULL,
        reservation_date DATETIME NOT NULL,
        last_modified DATETIME NOT NULL, 
        check_in_date DATETIME NOT NULL, 
        check_out_date DATETIME NOT NULL, 
        payment_status ENUM('Not Paid', 'Partially Paid', 'Fully Paid') NOT NULL,
        total_reservation_cost INT NOT NULL,
        reservation_status ENUM('Pending', 'Confirmed', 'Cancelled', 'Expired') NOT NULL,
        guest_id VARCHAR(12) NOT NULL, 
        room_id VARCHAR(11) NOT NULL, 
        
        PRIMARY KEY (reservation_id),
        KEY IDX_guest_id (guest_id),
        KEY IDX_room_id (room_id),
        
        CONSTRAINT reservedrooms_ibfk_guest_id FOREIGN KEY(guest_id) REFERENCES guests(guest_id),
        CONSTRAINT reservedrooms_ibfk_room_id FOREIGN KEY(room_id) REFERENCES rooms(room_id), 
        
        CONSTRAINT valid_check_in_out_dates_reserved_rooms CHECK (check_in_date < check_out_date)
        )""")

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS bookedrooms(
        booking_id VARCHAR(11) NOT NULL,
        check_in_status ENUM('In Progress', 'Finished') NOT NULL, 
        check_in_date DATETIME NOT NULL, 
        check_out_date DATETIME NOT NULL, 
        actual_check_in_date DATETIME NOT NULL,
        actual_check_out_date DATETIME,
        guest_id VARCHAR(12) NOT NULL, 
        room_id VARCHAR(11) NOT NULL, 
        
        PRIMARY KEY (booking_id),
        KEY IDX_guest_id (guest_id),
        KEY IDX_room_id (room_id),
        
        CONSTRAINT bookedrooms_ibfk_guest_id FOREIGN KEY(guest_id) REFERENCES guests(guest_id),
        CONSTRAINT bookedrooms_ibfk_room_id FOREIGN KEY(room_id) REFERENCES rooms(room_id), 
        
        CONSTRAINT valid_actual_check_in_out_dates_booked_rooms CHECK (actual_check_in_date < actual_check_out_date),
        CONSTRAINT valid_check_in_dates_booked_rooms CHECK (check_in_date <= actual_check_in_date),
        CONSTRAINT valid_check_in_out_dates_booked_rooms CHECK (check_in_date < check_out_date)
        )""")

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS paidrooms(
        payment_id VARCHAR(12) NOT NULL,
        payment_type ENUM('Cash', 'GCash', 'Maya', 'Bank Transfer', 'Others') NOT NULL, 
        amount INT NOT NULL, 
        transaction_date DATETIME NOT NULL, 
        guest_id VARCHAR(12) NOT NULL, 
        room_id VARCHAR(11) NOT NULL, 
        
        PRIMARY KEY (payment_id),
        KEY guest_id_idx (guest_id),
        KEY room_id_idx (room_id),
        
        CONSTRAINT paidrooms_ibfk_guest_id FOREIGN KEY(guest_id) REFERENCES guests(guest_id),
        CONSTRAINT paidrooms_ibfk_room_id FOREIGN KEY(room_id) REFERENCES rooms(room_id)
        )""")

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS services(
        service_id VARCHAR(11) NOT NULL,
        service_name VARCHAR(20) NOT NULL, 
        rate INT NOT NULL, 
        is_active TINYINT NOT NULL,
        
        PRIMARY KEY (service_id),
        
        UNIQUE KEY UC_service_name (service_name)
        )""")

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS availedservices(
        avail_id VARCHAR(12) NOT NULL,
        avail_date DATETIME NOT NULL,
        avail_status ENUM('Active', 'Cancelled', 'Completed') NOT NULL,
        quantity INT NOT NULL,
        guest_id VARCHAR(12) NOT NULL, 
        service_id VARCHAR(11) NOT NULL, 
        
        PRIMARY KEY (avail_id),
        KEY IDX_guest_id (guest_id),
        KEY IDX_service_id (service_id),
        
        CONSTRAINT availedservices_ibfk_guest_id FOREIGN KEY(guest_id) REFERENCES guests(guest_id),
        CONSTRAINT availedservices_ibfk_service_id FOREIGN KEY (service_id) REFERENCES services (service_id)
        
        )""")
