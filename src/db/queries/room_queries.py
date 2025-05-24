

class RoomQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def get_room_number_from_room_id(self, room_id):
        sql = "SELECT rooms.room_number FROM rooms WHERE room_id=%s AND is_active=1;"
        values = (room_id,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_room_details(self, room_number):
        sql = "SELECT * FROM rooms WHERE rooms.room_number=%s AND rooms.is_active=%s;"
        values = (room_number, 1)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result if result else None

    def check_if_image_is_used_by_many_rooms(self, image_file_name):
        sql = "SELECT CASE WHEN COUNT(*) > 1 THEN 1 ELSE 0 END FROM rooms WHERE image_file_name = %s AND is_active = 1"
        values = (image_file_name,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return True if result[0] else False

    def check_if_room_number_exists(self, room_number):
        sql = "SELECT 1 FROM rooms WHERE rooms.room_number=%s AND rooms.is_active = 1 LIMIT 1;"
        values = (room_number,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_room_image(self, room_number):
        sql = "SELECT rooms.image_file_name FROM rooms WHERE rooms.room_number=%s AND rooms.is_active=%s"
        values = (room_number, 1)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

    def has_available_room(self):
        sql = f"""SELECT COUNT(*) FROM rooms WHERE rooms.availability_status=%s"""
        values = ('available',)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()[0]

        if result > 0:
            return True
        else:
            return False

    def set_room_status(self, room_id, room_status, set_type="final"):

        sql = """UPDATE rooms SET rooms.availability_status=%s WHERE rooms.room_id=%s;"""
        values = (room_status, room_id)

        self.cursor.execute(sql, values)

        if set_type == "final":
            self.db.commit()

        # If set_type == "temporary", don't commit to the database!

    def refresh_all_room_status(self):
        sql = """SELECT 
                  r.room_id,
                  COALESCE(
                    CASE
                      WHEN rr.reservation_status = 'confirmed' AND br.check_in_status != 'checked out' THEN 'occupied'
                      WHEN rr.reservation_status = 'pending' THEN 'reserved'
                    END,
                    'available'
                  ) AS current_status
                FROM rooms r
                LEFT JOIN reservedrooms rr 
                  ON r.room_id = rr.room_id
                  AND NOW() BETWEEN rr.check_in_date AND rr.check_out_date
                  AND rr.reservation_status IN ('pending', 'confirmed')
                LEFT JOIN bookedrooms br
                  ON r.room_id = br.room_id
                  AND NOW() BETWEEN br.check_in_date AND br.check_out_date
                WHERE r.is_active = 1;"""

        self.cursor.execute(sql)

        result = self.cursor.fetchall()

        current_all_room_status = self.get_all_room_status()

        for i in range(len(result)):
            if result[i][0] == current_all_room_status[i][0] and result[i][1] != current_all_room_status[i][1] :
                self.set_room_status(result[i][0], result[i][1], set_type="final")

    def get_all_room_status(self):
        sql = "SELECT rooms.room_id, rooms.availability_status FROM rooms WHERE rooms.is_active=1"

        self.cursor.execute(sql)

        result = self.cursor.fetchall()

        return result

    def get_room_type(self, room_id):
        sql = "SELECT rooms.room_type FROM rooms WHERE rooms.room_id=%s"
        values = (room_id,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_latest_room_id(self):

        self.cursor.execute("""SELECT room_id FROM rooms
            ORDER BY CAST(SUBSTRING(room_id, 6) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "room-000000"
        else:
            return result[0]

    def get_rooms_from_room_type(self, room_type):

        sql = f"""SELECT rooms.room_id, rooms.room_number, rooms.room_type, rooms.daily_rate, rooms.availability_status, 
                        rooms.capacity
                        FROM rooms
                        WHERE rooms.room_type=%s AND rooms.is_active=1
                        ORDER BY rooms.room_id ASC;"""

        values = (room_type,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_all_rooms(self, enable_pagination=False, room_status=None, max_room_per_page=5, current_page_number=1,
                      sort_by="room_number", sort_type="ASC", search_input=None):

        if sort_by == "status" and enable_pagination:
            sort_by = "availability_status"

        if search_input and enable_pagination:
            search_input_query = """ AND (
                      rooms.room_number LIKE %s OR
                      rooms.room_type LIKE %s OR
                      CAST(rooms.daily_rate AS CHAR) LIKE %s OR
                      rooms.availability_status LIKE %s OR
                      CAST(rooms.capacity AS CHAR) LIKE %s
                    )"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input)
        else:
            search_input_query = ""
            values = ()

        # Maintenance still not in DB, configure later
        if room_status == "Maintenance":
            room_status = None

        if not room_status or room_status == "All status":
            sql = f"""SELECT rooms.room_number, rooms.room_type, rooms.daily_rate, rooms.availability_status, 
                    rooms.capacity, rooms.image_file_name
                    FROM rooms
                    WHERE is_active=1 {search_input_query}
                    """

        else:
            sql = f"""SELECT rooms.room_number, rooms.room_type, rooms.daily_rate, rooms.availability_status, 
                                rooms.capacity, rooms.image_file_name
                                FROM rooms
                                WHERE rooms.availability_status='{room_status.lower()}' AND is_active=1 {search_input_query}
                                """

        if enable_pagination:
            sql += f""" ORDER BY rooms.{sort_by} {sort_type} LIMIT {max_room_per_page}
                    OFFSET {max_room_per_page * (current_page_number - 1)}"""

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_room_count(self, availability_status, search_input=None):
        if availability_status not in ["All", "Available", "Reserved", "Occupied", "Maintenance", "Not Available"]:
            raise ValueError(f"Invalid availability status: {availability_status}.\n"
                             "Must be 'All', 'Available', 'Reserved', 'Occupied', or 'Maintenance', or 'Not Available'.")

        if search_input:
            search_input_query = """AND (
                      rooms.room_number LIKE %s OR
                      rooms.room_type LIKE %s OR
                      CAST(rooms.daily_rate AS CHAR) LIKE %s OR
                      rooms.availability_status LIKE %s OR
                      CAST(rooms.capacity AS CHAR) LIKE %s
                    )"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input)
        else:
            search_input_query = ""
            values = ()

        if availability_status == "All":
            sql = f"SELECT COUNT(*) FROM rooms WHERE is_active=1 {search_input_query}"
        else:
            sql = f"SELECT COUNT(*) FROM rooms WHERE availability_status=%s AND is_active=1 {search_input_query}"
            values = (availability_status,) + values

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()[0]

        return result

    def add_room(self, room_information):
        sql = """INSERT INTO rooms
                (room_id, room_number, room_type, daily_rate, availability_status, capacity, is_active, image_file_name) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)"""

        latest_room_id = self.get_latest_room_id()

        new_room_id = f"room-{int(latest_room_id[6:]) + 1:06}"

        values = (new_room_id,
                  room_information['room_number'],
                  room_information['room_type'],
                  room_information['daily_rate'],
                  'available',
                  room_information['capacity'],
                  True,
                  room_information['image_file_name'])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_room(self, old_room_number, room_information):
        sql = """UPDATE rooms SET room_number=%s, room_type=%s, daily_rate=%s,
        capacity=%s, image_file_name=%s WHERE room_number=%s AND is_active=1"""

        values = (room_information['room_number'],
                  room_information['room_type'],
                  room_information['daily_rate'],
                  room_information['capacity'],
                  room_information['image_file_name'],
                  old_room_number)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_room(self, room_number):

        sql = "UPDATE rooms SET is_active=%s, image_file_name=%s WHERE room_number=%s"
        values = (0, None, room_number)

        self.cursor.execute(sql, values)
        self.db.commit()
