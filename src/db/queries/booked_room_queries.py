from datetime import datetime


class BookedRoomQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def set_check_out_booking(self, booking_id):
        sql = "UPDATE bookedrooms SET check_in_status=%s, actual_check_out_date=%s WHERE booking_id=%s"
        values = ('checked out', datetime.now(), booking_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_all_bookings(self, sort_by="Booking ID", sort_type="Ascending", view_type="Bookings"):

        sort_by_dict = {"Booking ID": "bookedrooms.booking_id",
                        "Name": "guests.name",
                        "Room No.": "rooms.room_number",
                        "Room Type": "rooms.room_type",
                        "Check-in Date": "bookedrooms.actual_check_in_date",
                        "Check-out Date": "bookedrooms.check_out_date"}

        sort_type_dict = {"Ascending": "ASC", "Descending": "DESC"}

        view_type_dict = {"Bookings": "WHERE bookedrooms.check_in_status = 'in progress'",
                          "Past Bookings": "WHERE bookedrooms.check_in_status = 'checked out'",
                          "All": ""}

        sql = f"""SELECT bookedrooms.booking_id, guests.name, rooms.room_number, rooms.room_type, 
                        bookedrooms.actual_check_in_date, bookedrooms.check_out_date, bookedrooms.check_in_status
                        FROM bookedrooms
                        JOIN guests ON bookedrooms.guest_id = guests.guest_id
                        JOIN rooms ON bookedrooms.room_number = rooms.room_number
                        {view_type_dict[view_type]}
                        ORDER BY {sort_by_dict[sort_by]} {sort_type_dict[sort_type]};"""

        self.cursor.execute(sql)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

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
                (booking_id, check_in_status, check_in_date, check_out_date, actual_check_in_date, 
                actual_check_out_date, guest_id, room_number) VALUES
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
                  booked_room_information["room_number"])

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
