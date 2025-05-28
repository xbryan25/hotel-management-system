from datetime import datetime

from pymysql.cursors import DictCursor


class ReservedRoomQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def get_count_of_reservation_status(self, view_type='Today'):
        if view_type == 'Today':
            sql = """SELECT reservation_status, COUNT(*) FROM hms_db.reservedrooms 
                        WHERE DATE(reservation_date) = CURDATE() GROUP BY reservation_status;"""
        elif view_type == 'This Week':
            sql = """SELECT reservation_status, COUNT(*) FROM hms_db.reservedrooms 
                        WHERE  YEARWEEK(reservation_date, 1) = YEARWEEK(CURDATE(), 1) GROUP BY reservation_status;"""
        elif view_type == 'This Month':
            sql = """SELECT reservation_status, COUNT(*) FROM hms_db.reservedrooms 
                        WHERE MONTH(reservation_date) = MONTH(CURDATE())
                            AND YEAR(reservation_date) = YEAR(CURDATE())
                        GROUP BY reservation_status;"""
        elif view_type == 'This Year':
            sql = """SELECT reservation_status, COUNT(*) FROM hms_db.reservedrooms
                        WHERE YEAR(reservation_date) = YEAR(CURDATE())
                    GROUP BY reservation_status;"""
        else:
            sql = """SELECT reservation_status, COUNT(*) FROM hms_db.reservedrooms GROUP BY reservation_status;"""

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result

    def update_expired_reservations(self):
        sql = """UPDATE reservedrooms
                SET reservation_status = %s
                WHERE check_out_date < NOW()
                  AND reservation_status = %s;"""
        values = ('Expired', 'Pending')

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_all_check_in_and_check_out_of_room(self, room_id):
        sql = """SELECT reservedrooms.check_in_date, reservedrooms.check_out_date FROM reservedrooms 
                    WHERE reservedrooms.room_id=%s AND reservedrooms.reservation_status = %s AND
                    (NOW() < reservedrooms.check_in_date OR
                        NOW() BETWEEN reservedrooms.check_in_date AND reservedrooms.check_out_date)"""

        values = (room_id, 'Pending')

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_num_of_reservations_from_room(self, room_id):
        sql = """SELECT COUNT(*) FROM reservedrooms WHERE reservedrooms.room_id=%s AND 
                    reservedrooms.reservation_status=%s"""

        values = (room_id, 'Pending')

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

    def set_reservation_status(self, reservation_status, reservation_id):
        sql = "UPDATE reservedrooms SET reservation_status=%s WHERE reservation_id=%s"
        values = (reservation_status, reservation_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def set_payment_status(self, reservation_id, payment_status):
        sql = "UPDATE reservedrooms SET payment_status=%s WHERE reservation_id=%s"
        values = (payment_status, reservation_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_specific_reservation_details(self, column, reservation_id):
        allowed_columns = {'reservation_date', 'check_in_date', 'check_out_date', 'payment_status',
                           'total_reservation_cost', 'reservation_status', 'guest_id', 'room_id'}

        if column not in allowed_columns:
            raise ValueError(f"Invalid column name: {column}")

        sql = f"SELECT reservedrooms.{column} FROM reservedrooms WHERE reservation_id = %s"
        values = (reservation_id,)

        self.cursor.execute(sql, values)
        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_reservation_details(self, reservation_id):

        sql = f"""SELECT r.reservation_date, r.last_modified, r.check_in_date, r.check_out_date, r.payment_status, 
                    r.total_reservation_cost, r.reservation_status, r.guest_count, r.guest_id, r.room_id,
                    CAST(r.total_reservation_cost - COALESCE(SUM(p.amount), 0) AS SIGNED) AS remaining_balance
                    FROM reservedrooms r
                    JOIN guests ON r.guest_id = guests.guest_id
                    LEFT JOIN paidrooms p ON r.room_id = p.room_id
                    AND p.transaction_date BETWEEN r.reservation_date AND r.check_in_date
                    WHERE r.reservation_id = %s
                    GROUP BY r.reservation_id"""

        values = (reservation_id,)

        # Used a DictCursor here as there are many results
        with self.db.cursor(DictCursor) as dict_cursor:
            dict_cursor.execute(sql, values)

            result = dict_cursor.fetchone()

        return result if result else None

    def get_all_reservations(self, enable_pagination=False, max_reservations_per_page=20, current_page_number=1,
                             view_type="Reservations", sort_by="Reservation ID", sort_type="Ascending", search_input=None,
                             billing_view_mode=False):

        sort_by_dict = {"Reservation ID": "reservedrooms.reservation_id",
                        "Name": "guests.name",
                        "Room No.": "rooms.room_number",
                        "Room Type": "rooms.room_type",
                        "Check-In Date": "reservedrooms.check_in_date",
                        "Check-Out Date": "reservedrooms.check_out_date",
                        "Status": "payment_status",
                        "Total Reservation Cost": "reservedrooms.total_reservation_cost",
                        "Remaining Balance": "remaining_balance"}

        sort_type_dict = {"Ascending": "ASC", "Descending": "DESC"}

        view_type_dict = {"Reservations": "WHERE reservedrooms.reservation_status = 'Pending'",
                          "Past Reservations": "WHERE reservedrooms.reservation_status IN ('Confirmed', 'Cancelled', 'Expired')",
                          "Billings": """WHERE reservedrooms.payment_status IN ('Not Paid', 'Partially Paid') AND 
                                        reservedrooms.reservation_status='Pending'""",
                          "Past Billings": """WHERE reservedrooms.payment_status = 'Fully Paid' AND
                                        reservedrooms.reservation_status NOT IN ('Cancelled', 'Expired')""",
                          "All": "WHERE reservedrooms.reservation_status NOT IN ('Cancelled', 'Expired')"}

        if search_input and billing_view_mode:
            search_input_query = """ HAVING 
                        reservedrooms.reservation_id LIKE %s OR 
                        guests.name LIKE %s OR 
                        rooms.room_number LIKE %s OR 
                        reservedrooms.total_reservation_cost LIKE %s OR
                        CAST(reservedrooms.total_reservation_cost - COALESCE(SUM(paidrooms.amount), 0) AS CHAR) LIKE %s
            """

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input)
        elif search_input:
            search_input_query = """ AND 
                        (reservedrooms.reservation_id LIKE %s OR 
                        guests.name LIKE %s OR 
                        rooms.room_number LIKE %s OR 
                        rooms.room_type LIKE %s OR
                        DATE_FORMAT(check_in_date, '%%Y-%%m-%%d') LIKE %s OR
                        DATE_FORMAT(check_out_date, '%%Y-%%m-%%d') LIKE %s OR
                        CONCAT(DATE_FORMAT(check_in_date, '%%b %%d, %%Y'), ' - ', DATE_FORMAT(check_out_date, '%%b %%d, %%Y')) LIKE %s OR
                        reservedrooms.payment_status LIKE %s)"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input, search_input, search_input, search_input)
        else:
            search_input_query = ""
            values = ()

        if billing_view_mode:

            sql = f"""SELECT reservedrooms.reservation_id, guests.name, rooms.room_number, 
                            reservedrooms.total_reservation_cost, 
                            CAST(
                                CASE 
                                    WHEN reservedrooms.payment_status = 'Fully Paid' THEN 0
                                    ELSE reservedrooms.total_reservation_cost - COALESCE(SUM(paidrooms.amount), 0)
                                END AS SIGNED
                            ) AS remaining_balance,
                            reservedrooms.payment_status
                            FROM reservedrooms 
                            JOIN guests ON reservedrooms.guest_id = guests.guest_id
                            JOIN rooms ON reservedrooms.room_id = rooms.room_id
                            LEFT JOIN paidrooms ON reservedrooms.guest_id = paidrooms.guest_id 
                                AND reservedrooms.room_id = paidrooms.room_id
                                AND paidrooms.transaction_date BETWEEN reservedrooms.reservation_date AND reservedrooms.check_in_date
                            {view_type_dict[view_type]} 
                            GROUP BY reservedrooms.reservation_id, guests.name, rooms.room_number,
                                reservedrooms.total_reservation_cost, reservedrooms.payment_status
                            {search_input_query}
                            ORDER BY {sort_by_dict[sort_by]} {sort_type_dict[sort_type]}"""

        else:
            sql = f"""SELECT reservedrooms.reservation_id, guests.name, rooms.room_number, rooms.room_type, 
                            reservedrooms.check_in_date, reservedrooms.check_out_date, reservedrooms.payment_status,
                            reservedrooms.reservation_status
                            FROM reservedrooms 
                            JOIN guests ON reservedrooms.guest_id = guests.guest_id
                            JOIN rooms ON reservedrooms.room_id = rooms.room_id
                            {view_type_dict[view_type]}
                            {search_input_query}
                            ORDER BY {sort_by_dict[sort_by]} {sort_type_dict[sort_type]}"""

        if enable_pagination:
            sql += f""" LIMIT {max_reservations_per_page} 
                        OFFSET {max_reservations_per_page * (current_page_number - 1)}"""

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_reservation_count(self, view_type=None, search_input=None, billing_view_mode=False):

        view_type_dict = {"Reservations": "WHERE reservedrooms.reservation_status = 'pending'",
                          "Past Reservations": "WHERE reservedrooms.reservation_status IN ('confirmed', 'cancelled', 'expired')",
                          "Billings": "WHERE reservedrooms.payment_status IN ('not paid', 'partially paid')",
                          "Past Billings": "WHERE reservedrooms.payment_status = 'fully paid'",
                          "All": ""}

        if search_input and billing_view_mode:
            search_input_query = """ HAVING 
                        reservation_id LIKE %s OR 
                        name LIKE %s OR 
                        room_number LIKE %s OR 
                        CAST(total_reservation_cost AS CHAR) LIKE %s OR
                        remaining_balance LIKE %s
            """

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input)
        elif search_input:
            search_input_query = """ AND
                        (reservedrooms.reservation_id LIKE %s OR 
                        guests.name LIKE %s OR 
                        rooms.room_number LIKE %s OR 
                        rooms.room_type LIKE %s OR
                        DATE_FORMAT(check_in_date, '%%Y-%%m-%%d') LIKE %s OR
                        DATE_FORMAT(check_out_date, '%%Y-%%m-%%d') LIKE %s OR
                        CONCAT(DATE_FORMAT(check_in_date, '%%b %%d, %%Y'), ' - ', DATE_FORMAT(check_out_date, '%%b %%d, %%Y')) LIKE %s OR 
                        reservedrooms.payment_status LIKE %s)"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input, search_input, search_input, search_input)
        else:
            search_input_query = ""
            values = ()

        if billing_view_mode:
            sql = f"""SELECT COUNT(*) FROM (
                            SELECT reservedrooms.reservation_id AS reservation_id,
                            guests.name AS name,
                            rooms.room_number AS room_number,
                            reservedrooms.total_reservation_cost AS total_reservation_cost,
                            CAST(
                                reservedrooms.total_reservation_cost - 
                                COALESCE(SUM(paidrooms.amount), 0) AS CHAR
                            ) AS remaining_balance
                            FROM reservedrooms 
                            JOIN guests ON reservedrooms.guest_id = guests.guest_id
                            LEFT JOIN paidrooms ON reservedrooms.room_id = paidrooms.room_id
                                AND paidrooms.transaction_date BETWEEN reservedrooms.reservation_date AND reservedrooms.check_in_date
                            JOIN rooms ON reservedrooms.room_id = rooms.room_id
                            {view_type_dict[view_type]} 
                            GROUP BY reservation_id
                            {search_input_query}
                        ) AS sub"""
        else:
            sql = f"""SELECT COUNT(*)
                        FROM reservedrooms 
                        JOIN guests ON reservedrooms.guest_id = guests.guest_id
                        JOIN rooms ON reservedrooms.room_id = rooms.room_id
                        {view_type_dict[view_type]}
                        {search_input_query}"""

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()[0]

        return result

    def get_latest_reservation_id(self):

        self.cursor.execute("""SELECT reservation_id FROM reservedrooms
            ORDER BY CAST(SUBSTRING(reservation_id, 9) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "reserve-000000"
        else:
            return result[0]

    def add_reserved_room(self, reserved_room_information):
        sql = """INSERT INTO reservedrooms
                (reservation_id, reservation_date, last_modified, check_in_date, check_out_date, payment_status, 
                total_reservation_cost, reservation_status, guest_count, guest_id, room_id) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        latest_reservation_id = self.get_latest_reservation_id()

        new_reservation_id = f"reserve-{int(latest_reservation_id[9:]) + 1:06}"

        values = (new_reservation_id,
                  reserved_room_information["reservation_date"],
                  reserved_room_information["last_modified"],
                  reserved_room_information["check_in_date"],
                  reserved_room_information["check_out_date"],
                  reserved_room_information["payment_status"],
                  reserved_room_information["total_reservation_cost"],
                  reserved_room_information["reservation_status"],
                  reserved_room_information["guest_count"],
                  reserved_room_information["guest_id"],
                  reserved_room_information["room_id"])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_reserved_room(self, reservation_id, reserved_room_information, date_time_now=None):

        if not date_time_now:
            date_time_now = datetime.now()

        sql = """UPDATE reservedrooms SET last_modified=%s, check_in_date=%s, check_out_date=%s, 
                    total_reservation_cost=%s, room_id=%s, guest_count=%s
                    WHERE reservation_id=%s;"""

        values = (date_time_now,
                  reserved_room_information['check_in_date'],
                  reserved_room_information['check_out_date'],
                  reserved_room_information['total_reservation_cost'],
                  reserved_room_information['room_id'],
                  reserved_room_information['guest_count'],
                  reservation_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_reserved_room(self, identifier):
        sql = "DELETE FROM reservedrooms WHERE reservation_id=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()
