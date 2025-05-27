from datetime import datetime

from pymysql.cursors import DictCursor


class BookedRoomQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def update_elapsed_bookings(self):
        sql = """UPDATE bookedrooms SET check_in_status = %s, actual_check_out_date=check_out_date 
                    WHERE check_out_date < NOW() AND check_in_status = %s;"""
        values = ('Finished', 'In Progress')

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_booking_details(self, booking_id):

        sql = f"""SELECT b.check_in_status, b.check_in_date, b.check_out_date, b.actual_check_in_date,
                    b.actual_check_out_date, rr.reservation_id, rr.total_reservation_cost,
                    rr.guest_count, rr.last_modified, r.room_number, r.room_type, g.name, g.guest_id
                    FROM bookedrooms b
                    JOIN reservedrooms rr ON b.guest_id = rr.guest_id AND b.room_id = rr.room_id AND
                        b.check_in_date = rr.check_in_date AND b.check_out_date = rr.check_out_date 
                    JOIN rooms r ON b.room_id = r.room_id
                    JOIN guests g ON b.guest_id = g.guest_id
                    WHERE b.booking_id = %s"""

        values = (booking_id,)

        # Used a DictCursor here as there are many results
        with self.db.cursor(DictCursor) as dict_cursor:
            dict_cursor.execute(sql, values)

            result = dict_cursor.fetchone()

        return result if result else None


    def find_booking_by_guest_and_room(self, guest_id, room_id, check_in_date, check_out_date):
        sql = """SELECT * FROM bookedrooms WHERE bookedrooms.guest_id=%s AND bookedrooms.room_id=%s AND 
                bookedrooms.check_in_date=%s AND bookedrooms.check_out_date=%s"""

        values = (guest_id, room_id, check_in_date, check_out_date)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_num_of_bookings_from_room(self, room_id):
        sql = """SELECT COUNT(*) FROM bookedrooms WHERE bookedrooms.room_id=%s AND 
                    bookedrooms.check_in_status=%s"""

        values = (room_id, 'In Progress')

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_check_in_status_of_booking(self, booking_id):

        sql = """SELECT bookedrooms.check_in_status FROM bookedrooms WHERE bookedrooms.booking_id=%s"""

        values = (room_id,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

    def set_check_out_booking(self, booking_id):
        sql = "UPDATE bookedrooms SET check_in_status=%s, actual_check_out_date=%s WHERE booking_id=%s"
        values = ('Finished', datetime.now(), booking_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_all_bookings(self, max_bookings_per_page=20, current_page_number=1, view_type="Bookings",
                         sort_by="Booking ID", sort_type="Ascending", search_input=None):

        sort_by_dict = {"Booking ID": "bookedrooms.booking_id",
                        "Name": "guests.name",
                        "Room No.": "rooms.room_number",
                        "Room Type": "rooms.room_type",
                        "Check-In Date": "bookedrooms.actual_check_in_date",
                        "Check-Out Date": "bookedrooms.check_out_date"}

        sort_type_dict = {"Ascending": "ASC", "Descending": "DESC"}

        view_type_dict = {"Bookings": "WHERE bookedrooms.check_in_status = 'In Progress'",
                          "Past Bookings": "WHERE bookedrooms.check_in_status = 'Finished'",
                          "All": ""}

        if search_input:
            search_input_query = """ AND 
                        (bookedrooms.booking_id LIKE %s OR 
                        guests.name LIKE %s OR 
                        rooms.room_number LIKE %s OR 
                        rooms.room_type LIKE %s OR
                        DATE_FORMAT(actual_check_in_date, '%%Y-%%m-%%d') LIKE %s OR
                        DATE_FORMAT(check_out_date, '%%Y-%%m-%%d') LIKE %s OR
                        CONCAT(DATE_FORMAT(check_in_date, '%%b %%d, %%Y'), ' - ', DATE_FORMAT(check_out_date, '%%b %%d, %%Y')) LIKE %s)"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input, search_input, search_input)
        else:
            search_input_query = ""
            values = ()

        sql = f"""SELECT bookedrooms.booking_id, guests.name, rooms.room_number, rooms.room_type, 
                        bookedrooms.actual_check_in_date, bookedrooms.check_out_date, bookedrooms.check_in_status
                        FROM bookedrooms
                        JOIN guests ON bookedrooms.guest_id = guests.guest_id
                        JOIN rooms ON bookedrooms.room_id = rooms.room_id
                        {view_type_dict[view_type]}
                        {search_input_query}
                        ORDER BY {sort_by_dict[sort_by]} {sort_type_dict[sort_type]}"""

        sql += f""" LIMIT {max_bookings_per_page} OFFSET {max_bookings_per_page * (current_page_number - 1)}"""

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_booking_count(self, view_type=None, search_input=None):

        view_type_dict = {"Bookings": "WHERE bookedrooms.check_in_status = 'in progress'",
                          "Past Bookings": "WHERE bookedrooms.check_in_status = 'checked out'",
                          "All": ""}

        if search_input:
            search_input_query = """ AND 
                        (bookedrooms.booking_id LIKE %s OR 
                        guests.name LIKE %s OR 
                        rooms.room_number LIKE %s OR 
                        rooms.room_type LIKE %s OR
                        DATE_FORMAT(actual_check_in_date, '%%Y-%%m-%%d') LIKE %s OR
                        DATE_FORMAT(check_out_date, '%%Y-%%m-%%d') LIKE %s OR
                        CONCAT(DATE_FORMAT(check_in_date, '%%b %%d, %%Y'), ' - ', DATE_FORMAT(check_out_date, '%%b %%d, %%Y')) LIKE %s)"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input, search_input, search_input)
        else:
            search_input_query = ""
            values = ()

        sql = f"""SELECT COUNT(*)
                    FROM bookedrooms
                    JOIN guests ON bookedrooms.guest_id = guests.guest_id
                    JOIN rooms ON bookedrooms.room_id = rooms.room_id
                    {view_type_dict[view_type]}
                    {search_input_query}"""

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()[0]

        return result

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

        sql = f"""SELECT bookedrooms.booking_id, guests.name, bookedrooms.room_id,  bookedrooms.actual_{check_type}_date
                FROM bookedrooms 
                JOIN guests ON bookedrooms.guest_id = guests.guest_id
                WHERE DATE(bookedrooms.actual_{check_type}_date) = CURDATE();"""

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
                WHERE DATE(bookedrooms.actual_{check_type}_date) = CURDATE();"""

        self.cursor.execute(sql)

        result = self.cursor.fetchone()[0]

        return result

    def add_booked_room(self, booked_room_information):
        sql = """INSERT INTO bookedrooms
                (booking_id, check_in_status, check_in_date, check_out_date, actual_check_in_date, 
                actual_check_out_date, guest_id, room_id) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)"""

        latest_booking_id = self.get_latest_booking_id()

        new_booking_id = f"book-{int(latest_booking_id[6:]) + 1:06}"

        values = (new_booking_id,
                  booked_room_information["check_in_status"],
                  booked_room_information["check_in_date"],
                  booked_room_information["check_out_date"],
                  booked_room_information["actual_check_in_date"],
                  booked_room_information["actual_check_out_date"],
                  booked_room_information["guest_id"],
                  booked_room_information["room_id"])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_booked_room(self, old_booking_id, booked_room_information):
        sql = """UPDATE bookedrooms SET booking_id=%s, check_in_status=%s, check_in_date=%s, check_out_date=%s, 
        guest_id=%s, room_id=%s
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
