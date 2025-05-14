

class RoomQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def has_available_room(self):
        sql = f"""SELECT COUNT(*) FROM rooms WHERE rooms.availability_status=%s"""
        values = ('available',)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()[0]

        if result > 0:
            return True
        else:
            return False

    def set_room_status(self, room_number, room_status, set_type="final"):

        sql = """UPDATE rooms SET rooms.availability_status=%s WHERE rooms.room_number=%s;"""
        values = (room_status, room_number)

        self.cursor.execute(sql, values)

        if set_type == "final":
            self.db.commit()

        # If set_type == "temporary", don't commit to the database!

    def get_room_type(self, room_number):
        sql = "SELECT rooms.room_type FROM rooms WHERE rooms.room_number=%s"
        values = (room_number,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

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
            sql = f"""SELECT rooms.room_number, rooms.room_type, rooms.daily_rate, rooms.availability_status, 
                            rooms.capacity
                            FROM rooms
                            WHERE rooms.availability_status="available"
                            ORDER BY rooms.room_number ASC;"""

            self.cursor.execute(sql)
        else:
            sql = f"""SELECT rooms.room_number, rooms.room_type, rooms.daily_rate, rooms.availability_status, 
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

    def get_all_rooms(self, room_status=None):

        # Maintenance still not in DB, configure later
        if room_status == "Maintenance":
            room_status = None

        if not room_status or room_status == "All status":
            sql = f"""SELECT rooms.room_number, rooms.room_type, rooms.daily_rate, rooms.availability_status, 
                    rooms.capacity
                    FROM rooms
                    ORDER BY rooms.room_number ASC;"""

        else:
            sql = f"""SELECT rooms.room_number, rooms.room_type, rooms.daily_rate, rooms.availability_status, 
                                rooms.capacity
                                FROM rooms
                                WHERE rooms.availability_status='{room_status.lower()}'
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