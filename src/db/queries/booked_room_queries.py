

class BookedRoomQueries:
    def __init__(self, cursor):
        self.cursor = cursor

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
