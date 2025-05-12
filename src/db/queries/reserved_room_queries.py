

class ReservedRoomQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def set_confirmed_reservation(self, reservation_id):
        sql = "UPDATE reservedrooms SET reservation_status=%s WHERE reservation_id=%s"
        values = ('confirmed', reservation_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def set_payment_status(self, reservation_id, payment_status):
        sql = "UPDATE reservedrooms SET payment_status=%s WHERE reservation_id=%s"
        values = (payment_status, reservation_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_specific_reservation_details(self, column, reservation_id):
        allowed_columns = {'reservation_date', 'check_in_date', 'check_out_date', 'payment_status',
                           'total_reservation_cost', 'reservation_status', 'guest_id', 'room_number'}

        if column not in allowed_columns:
            raise ValueError(f"Invalid column name: {column}")

        sql = f"SELECT reservedrooms.{column} FROM reservedrooms WHERE reservation_id = %s"
        values = (reservation_id,)

        self.cursor.execute(sql, values)
        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_reservation_details(self, reservation_id):
        # TODO: Convert to dictionary soon

        sql = f"""SELECT r.reservation_date, r.check_in_date, r.check_out_date, r.payment_status, 
                    r.total_reservation_cost, r.reservation_status, r.guest_id, r.room_number,
                    CAST(r.total_reservation_cost - COALESCE(SUM(p.amount), 0) AS SIGNED) AS remaining_balance
                    FROM reservedrooms r
                    JOIN guests ON r.guest_id = guests.guest_id
                    LEFT JOIN paidrooms p ON r.room_number = p.room_number
                    AND p.transaction_date BETWEEN r.reservation_date AND r.check_in_date
                    WHERE r.reservation_id = %s
                    GROUP BY r.reservation_id"""

        values = (reservation_id,)

        self.cursor.execute(sql, values)
        result = self.cursor.fetchone()

        return result if result else None

    def get_all_reservations(self, sort_by="Reservation ID", sort_type="Ascending", view_type="Reservations",
                             billing_view_mode=False):

        sort_by_dict = {"Reservation ID": "reservedrooms.reservation_id",
                        "Name": "guests.name",
                        "Room No.": "rooms.room_number",
                        "Room Type": "rooms.room_type",
                        "Check-in Date": "reservedrooms.check_in_date",
                        "Check-out Date": "reservedrooms.check_out_date",
                        "Status": "payment_status"}

        sort_type_dict = {"Ascending": "ASC", "Descending": "DESC"}

        view_type_dict = {"Reservations": "WHERE reservedrooms.reservation_status = 'pending'",
                          "Past Reservations": "WHERE reservedrooms.reservation_status IN ('confirmed', 'cancelled', 'expired')",
                          "Billings": "WHERE r.payment_status IN ('not paid', 'partially paid')",
                          "Past Billings": "WHERE r.payment_status = 'fully paid'",
                          "All": ""}

        if billing_view_mode:

            sql = f"""SELECT r.reservation_id, guests.name, r.room_number, r.total_reservation_cost, 
                            CAST(r.total_reservation_cost - COALESCE(SUM(p.amount), 0) AS SIGNED) AS remaining_balance,
                            r.payment_status
                            FROM reservedrooms r
                            JOIN guests ON r.guest_id = guests.guest_id
                            LEFT JOIN paidrooms p ON r.room_number = p.room_number
                            AND p.transaction_date BETWEEN r.reservation_date AND r.check_in_date
                            {view_type_dict[view_type]}
                            GROUP BY r.reservation_id"""

        else:
            sql = f"""SELECT reservedrooms.reservation_id, guests.name, rooms.room_number, rooms.room_type, 
                                        reservedrooms.check_in_date, reservedrooms.check_out_date, reservedrooms.payment_status,
                                        reservedrooms.reservation_status
                                        FROM reservedrooms 
                                        JOIN guests ON reservedrooms.guest_id = guests.guest_id
                                        JOIN rooms ON reservedrooms.room_number = rooms.room_number
                                        {view_type_dict[view_type]}
                                        ORDER BY {sort_by_dict[sort_by]} {sort_type_dict[sort_type]};"""

        self.cursor.execute(sql)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result


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
                total_reservation_cost, reservation_status, guest_id, room_number) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

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
