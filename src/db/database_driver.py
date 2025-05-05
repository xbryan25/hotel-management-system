import pymysql
from datetime import date

from dotenv import load_dotenv
import os

from db.initialize_database import InitializeDatabase


load_dotenv()


class DatabaseDriver:

    def __init__(self):

        self.check_environment_variables()

        self.db = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database='hms_db'
        )

        self.cursor = self.db.cursor()

        InitializeDatabase(self.cursor)

    def get_latest_guest_id(self):

        self.cursor.execute("""SELECT guest_id FROM guests
            ORDER BY CAST(SUBSTRING(guest_id, 7) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "guest-000000"
        else:
            return result[0]

    def get_active_guests(self, sort_by, sort_type):

        sort_by_dict = {"Guest Name": "guests.name",
                        "Room Number": "rooms.room_number",
                        "Check In Date": "bookedrooms.check_in_date",
                        "Check Out Date": "bookedrooms.check_out_date",
                        "Room Type": "rooms.room_type",
                        "Amount Due": "rooms.room_type"}

        sort_type_dict = {"Ascending": "ASC", "Descending": "DESC"}

        sql = f"""SELECT guests.guest_id, guests.name, rooms.room_number, bookedrooms.check_in_date, 
                        bookedrooms.check_out_date, rooms.room_type
                        FROM guests
                        JOIN bookedrooms ON guests.guest_id = bookedrooms.guest_id
                        JOIN rooms ON bookedrooms.room_number = rooms.room_number
                        ORDER BY {sort_by_dict[sort_by]} {sort_type_dict[sort_type]};"""

        self.cursor.execute(sql)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_guest_details(self, guest_id):

        sql = f"""SELECT guests.guest_id, guests.name, guests.sex, guests.home_address, 
                        guests.email_address, guests.phone_number, guests.birth_date,
                        guests.government_id, guests.last_visit_date, guests.visit_count
                        FROM guests
                        WHERE guests.guest_id=%s;"""

        values = (guest_id,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result[0]

    def get_guest_id_from_name(self, guest_name):

        sql = f"""SELECT guests.guest_id
                    FROM guests
                    WHERE guests.name=%s;"""

        values = (guest_name,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0]

    def add_guest(self, guest_information):

        # SQL avoids duplication of names
        sql = """INSERT INTO guests 
                (guest_id, name, sex, home_address, email_address, phone_number, 
                birth_date, government_id, visit_count) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name = name"""

        latest_guest_id = self.get_latest_guest_id()

        new_guest_id = f"guest-{int(latest_guest_id[7:]) + 1:06}"

        values = (new_guest_id,
                  guest_information["name"],
                  guest_information["sex"],
                  guest_information["home_address"],
                  guest_information["email_address"],
                  guest_information["phone_number"],
                  guest_information["birth_date"],
                  guest_information["government_id"],
                  1)

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_guest(self, old_guest_id, guest_information):
        sql = """UPDATE guests 
                SET guest_id=%s, name=%s, sex=%s, home_address=%s, email_address=%s, phone_number=%s, 
                birth_date=%s, government_id=%s, last_visit_date=%s, visit_count=%s WHERE 
                guest_id=%s"""

        values = (guest_information[0],
                  guest_information[1],
                  guest_information[2],
                  guest_information[3],
                  guest_information[4],
                  guest_information[5],
                  guest_information[6],
                  guest_information[7],
                  guest_information[8],
                  guest_information[9],
                  old_guest_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_guest(self, identifier_type, identifier):

        sql = ""
        values = (identifier.strip(),)

        if identifier_type == "guest_id":
            sql = "DELETE FROM guests WHERE guest_id=%s"
        elif identifier_type == "name":
            sql = "DELETE FROM guests WHERE name=%s"

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_latest_room_number(self):

        self.cursor.execute("""SELECT room_number FROM rooms
            ORDER BY CAST(SUBSTRING(room_number, 6) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "room-0000"
        else:
            return result[0]

    def get_available_rooms(self, room_type=None):
        if not room_type:
            sql = f"""SELECT rooms.room_number, rooms.room_type, rooms.price, rooms.availability_status, 
                            rooms.capacity
                            FROM rooms
                            WHERE rooms.availability_status="available"
                            ORDER BY rooms.room_number ASC;"""

            self.cursor.execute(sql)
        else:
            sql = f"""SELECT rooms.room_number, rooms.room_type, rooms.price, rooms.availability_status, 
                            rooms.capacity
                            FROM rooms
                            WHERE rooms.room_type=%s
                            AND rooms.availability_status="available"
                            ORDER BY rooms.room_number ASC;"""

            values = (room_type,)

            self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_all_rooms(self):

        sql = f"""SELECT rooms.room_number, rooms.room_type, rooms.price, rooms.availability_status, 
                rooms.capacity
                FROM rooms
                ORDER BY rooms.room_number ASC;"""

        self.cursor.execute(sql)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_room_count(self, availability_status):
        if availability_status not in ["available", "reserved", "occupied"]:
            raise ValueError(f"Invalid availability status: {availability_status}. Must be 'available', 'reserved', or 'occupied'.")

        sql = "SELECT COUNT(*) FROM rooms WHERE availability_status=%s;"
        values = (availability_status,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()[0]

        return result

    def add_room(self, room_information):
        sql = """INSERT INTO rooms
                (room_number, room_type, price, availability_status, capacity) VALUES
                (%s, %s, %s, %s, %s)"""

        latest_room_number = self.get_latest_room_number()

        new_room_number = f"room-{int(latest_room_number[6:]) + 1:04}"

        values = (new_room_number,
                  room_information[0],
                  room_information[1],
                  room_information[2],
                  room_information[3])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_room(self, old_room_number, room_information):
        sql = """UPDATE rooms SET room_number=%s, room_type=%s, price=%s, 
        availability_status=%s, capacity=%s WHERE room_number=%s"""

        values = (room_information[0],
                  room_information[1],
                  room_information[2],
                  room_information[3],
                  room_information[4],
                  old_room_number)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_room(self, identifier):

        sql = "DELETE FROM rooms WHERE room_number=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_latest_service_id(self):

        self.cursor.execute("""SELECT service_id FROM services
            ORDER BY CAST(SUBSTRING(service_id, 9) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "service-000"
        else:
            return result[0]

    def get_all_services(self):
        self.cursor.execute("""SELECT * FROM services;""")

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def add_service(self, service_information):
        sql = """INSERT INTO services
                (service_id, service_name, rate) VALUES
                (%s, %s, %s)"""

        latest_service_id = self.get_latest_service_id()

        new_service_id = f"service-{int(latest_service_id[9:]) + 1:03}"

        values = (new_service_id,
                  service_information[0],
                  service_information[1])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_service(self, old_service_id, service_information):
        sql = """UPDATE services SET service_id=%s, service_name=%s, rate=%s
        WHERE service_id=%s;"""

        values = (service_information[0],
                  service_information[1],
                  service_information[2],
                  old_service_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_service(self, identifier):

        sql = "DELETE FROM services WHERE service_id=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_latest_avail_id(self):

        self.cursor.execute("""SELECT avail_id FROM availedservices
            ORDER BY CAST(SUBSTRING(avail_id, 7) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "avail-000000"
        else:
            return result[0]

    def add_availed_services(self, availed_service_information, guest_id):

        for service_id, quantity in availed_service_information.items():

            sql = """INSERT INTO availedservices
                    (avail_id, avail_date, quantity, guest_id, service_id) VALUES
                    (%s, %s, %s, %s, %s)"""

            latest_avail_id = self.get_latest_avail_id()

            new_avail_id = f"avail-{int(latest_avail_id[9:]) + 1:06}"

            values = (new_avail_id,
                      date.today(),
                      quantity,
                      guest_id,
                      service_id)

            self.cursor.execute(sql, values)
            self.db.commit()

    def update_availed_service(self, old_avail_id, availed_service_information):
        sql = """UPDATE availedservices SET avail_id=%s, avail_date=%s, guest_id=%s, service_id=%s
        WHERE avail_id=%s;"""

        values = (availed_service_information[0],
                  availed_service_information[1],
                  availed_service_information[2],
                  availed_service_information[3],
                  old_avail_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_availed_service(self, identifier):

        sql = "DELETE FROM availedservices WHERE avail_id=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_latest_payment_id(self):

        self.cursor.execute("""SELECT payment_id FROM paidrooms
            ORDER BY CAST(SUBSTRING(payment_id, 6) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "paid-000000"
        else:
            return result[0]

    def add_paid_room(self, paid_room_information):
        sql = """INSERT INTO paidrooms
                (payment_id, payment_type, amount, transaction_date, guest_id, room_number) VALUES
                (%s, %s, %s, %s, %s, %s)"""

        latest_payment_id = self.get_latest_payment_id()

        new_payment_id = f"paid-{int(latest_payment_id[9:]) + 1:06}"

        values = (new_payment_id,
                  paid_room_information[0],
                  paid_room_information[1],
                  paid_room_information[2],
                  paid_room_information[3],
                  paid_room_information[4])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_paid_room(self, old_payment_id, paid_room_information):
        sql = """UPDATE paidrooms SET payment_id=%s, payment_type=%s, amount=%s, transaction_date=%s, guest_id=%s, room_number=%s
        WHERE payment_id=%s;"""

        values = (paid_room_information[0],
                  paid_room_information[1],
                  paid_room_information[2],
                  paid_room_information[3],
                  paid_room_information[4],
                  paid_room_information[5],
                  old_payment_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_paid_room(self, identifier):

        sql = "DELETE FROM paidrooms WHERE payment_id=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_latest_reservation_id(self):

        self.cursor.execute("""SELECT reservation_id FROM reservedrooms
            ORDER BY CAST(SUBSTRING(reservation_id, 9) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "reserve-000000"
        else:
            return result[0]

    def get_all_reservations(self):
        # Gets all future reservations, the order of the results are based on the check_in_date

        sql = f"""SELECT reservedrooms.reservation_id, guests.name, rooms.room_number, rooms.room_type, 
                reservedrooms.check_in_date, reservedrooms.check_out_date, reservedrooms.payment_status
                FROM reservedrooms 
                JOIN guests ON reservedrooms.guest_id = guests.guest_id
                JOIN rooms ON reservedrooms.room_number = rooms.room_number
                ORDER BY reservedrooms.check_in_date ASC;"""

        self.cursor.execute(sql)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def add_reserved_room(self, reserved_room_information):
        sql = """INSERT INTO reservedrooms
                (reservation_id, reservation_date, check_in_date, check_out_date, payment_status, total_reservation_cost,
                guest_id, room_number) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)"""

        latest_reservation_id = self.get_latest_reservation_id()

        new_reservation_id = f"reserve-{int(latest_reservation_id[9:]) + 1:06}"

        values = (new_reservation_id,
                  reserved_room_information["reservation_date"],
                  reserved_room_information["check_in_date"],
                  reserved_room_information["check_out_date"],
                  reserved_room_information["payment_status"],
                  reserved_room_information["total_reservation_cost"],
                  reserved_room_information["guest_id"],
                  reserved_room_information["room_number"])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_reserved_room(self, old_reservation_id, reserved_room_information):
        sql = """UPDATE reservedrooms SET reservation_id=%s, reservation_date=%s, check_in_date=%s, check_out_date=%s, 
        payment_status=%s, guest_id=%s, room_number=%s
        WHERE reservation_id=%s;"""

        values = (reserved_room_information[0],
                  reserved_room_information[1],
                  reserved_room_information[2],
                  reserved_room_information[3],
                  reserved_room_information[4],
                  reserved_room_information[5],
                  reserved_room_information[6],
                  old_reservation_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_reserved_room(self, identifier):
        sql = "DELETE FROM reservedrooms WHERE reservation_id=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_latest_booking_id(self):

        self.cursor.execute("""SELECT booking_id FROM bookedrooms
            ORDER BY CAST(SUBSTRING(booking_id, 6) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "book-000000"
        else:
            return result[0]

    def get_all_booked_room_today(self, check_type):

        if check_type not in ["check_in", "check_out"]:
            raise ValueError(f"Invalid check_type: {check_type}. Must be 'check_in' or 'check_out'.")

        sql = f"""SELECT bookedrooms.booking_id, guests.name, bookedrooms.room_number,  bookedrooms.{check_type}_date
                FROM bookedrooms 
                JOIN guests ON bookedrooms.guest_id = guests.guest_id
                WHERE bookedrooms.{check_type}_date = CURDATE();"""

        self.cursor.execute(sql)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_count_all_booked_room_today(self, check_type):

        if check_type not in ["check_in", "check_out"]:
            raise ValueError(f"Invalid check_type: {check_type}. Must be 'check_in' or 'check_out'.")

        sql = f"""SELECT COUNT(*)
                FROM bookedrooms 
                JOIN guests ON bookedrooms.guest_id = guests.guest_id
                WHERE bookedrooms.{check_type}_date = CURDATE();"""

        self.cursor.execute(sql)

        result = self.cursor.fetchone()[0]

        return result

    def add_booked_room(self, booked_room_information):
        sql = """INSERT INTO bookedrooms
                (booking_id, check_in_status, check_in_date, check_out_date, guest_id, room_number) VALUES
                (%s, %s, %s, %s, %s, %s)"""

        latest_booking_id = self.get_latest_booking_id()

        new_booking_id = f"book-{int(latest_booking_id[6:]) + 1:06}"

        values = (new_booking_id,
                  booked_room_information[0],
                  booked_room_information[1],
                  booked_room_information[2],
                  booked_room_information[3],
                  booked_room_information[4])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_booked_room(self, old_booking_id, booked_room_information):
        sql = """UPDATE bookedrooms SET booking_id=%s, check_in_status=%s, check_in_date=%s, check_out_date=%s, 
        guest_id=%s, room_number=%s
        WHERE booking_id=%s;"""

        values = (booked_room_information[0],
                  booked_room_information[1],
                  booked_room_information[2],
                  booked_room_information[3],
                  booked_room_information[4],
                  booked_room_information[5],
                  old_booking_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_booked_room(self, identifier):
        sql = "DELETE FROM bookedrooms WHERE booking_id=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()

    def close_connection(self):
        self.db.close()

    @staticmethod
    def check_environment_variables():
        if not all([os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD")]):
            raise EnvironmentError("Missing one or more required DB environment variables.")
