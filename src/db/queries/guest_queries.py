
from datetime import date


class GuestQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def get_top_paying_guests(self, view_type):

        sql = """SELECT guests.name, SUM(paidrooms.amount) as total FROM guests JOIN paidrooms ON guests.guest_id = paidrooms.guest_id """

        if view_type == 'Today':
            sql += """WHERE DATE(paidrooms.transaction_date) = CURDATE() """

        elif view_type == 'This Week':
            sql += """WHERE YEARWEEK(paidrooms.transaction_date, 1) = YEARWEEK(CURDATE(), 1) """

        elif view_type == 'This Month':
            sql += """WHERE MONTH(paidrooms.transaction_date) = MONTH(CURDATE())
                                AND YEAR(paidrooms.transaction_date) = YEAR(CURDATE()) """

        elif view_type == 'This Year':
            sql += """WHERE YEAR(paidrooms.transaction_date) = YEAR(CURDATE()) """

        sql += """GROUP BY guests.name ORDER BY total DESC LIMIT 5;"""

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result

    def update_guest_visit_count_and_last_visit_date(self, guest_id):
        sql = "UPDATE guests SET last_visit_date=%s, visit_count=visit_count+1 WHERE guest_id=%s"
        values = (date.today(), guest_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_latest_guest_id(self):

        self.cursor.execute("""SELECT guest_id FROM guests
            ORDER BY CAST(SUBSTRING(guest_id, 7) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "guest-000000"
        else:
            return result[0]

    def get_all_guests(self, max_guests_per_page=20, current_page_number=1, show_type="All Guests",
                       sort_by="Guest Name", sort_type="Ascending", search_input=None):

        guest_table_columns = {"Guest Name": "name",
                               "Phone Number": "phone_number",
                               "Last Visit Date": "last_visit_date",
                               "Visit Count": "visit_count"}

        sort_type_formatted = {"Ascending": "ASC", "Descending": "DESC"}

        if search_input:
            search_input_query = """ HAVING
                      guests.name LIKE %s OR
                      guests.phone_number LIKE %s OR
                      guests.last_visit_date LIKE %s OR
                      CAST(guests.visit_count AS CHAR) LIKE %s OR
                      CAST(remaining_balance AS CHAR) LIKE %s"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input)
        else:
            search_input_query = ""
            values = ()

        if show_type == "With Reservations":

            sql = f"""SELECT guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, 
                        guests.visit_count,
                        CAST(COALESCE(SUM(reservedrooms.total_reservation_cost), 0) - COALESCE(paid.total_paid, 0) AS SIGNED) AS remaining_balance
                        FROM guests
                        
                        JOIN reservedrooms ON guests.guest_id = reservedrooms.guest_id
                          AND reservedrooms.reservation_status = 'Pending'
                          
                        LEFT JOIN (
                            SELECT guest_id, SUM(amount) AS total_paid
                            FROM paidrooms
                            GROUP BY guest_id
                        ) AS paid ON guests.guest_id = paid.guest_id
                        
                        GROUP BY guests.guest_id, guests.name, guests.phone_number, 
                                 guests.last_visit_date, guests.visit_count
                        {search_input_query}
                        """

        elif show_type == "Currently Staying":

            sql = f"""SELECT guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, 
                        guests.visit_count, 
                        CAST(COALESCE(reservations.total_cost, 0) -  COALESCE(payments.total_paid, 0) AS SIGNED) AS remaining_balance
                        FROM guests
                        
                        JOIN (
                            SELECT guest_id
                            FROM bookedrooms
                            WHERE check_in_status = 'In Progress'
                            GROUP BY guest_id
                        ) AS bookings ON guests.guest_id = bookings.guest_id
                        
                        LEFT JOIN (
                            SELECT guest_id, SUM(total_reservation_cost) AS total_cost
                            FROM reservedrooms
                            WHERE reservation_status IN ('Pending', 'Confirmed')
                            GROUP BY guest_id
                        ) AS reservations ON guests.guest_id = reservations.guest_id
                        
                        LEFT JOIN (
                            SELECT guest_id, SUM(amount) AS total_paid
                            FROM paidrooms
                            GROUP BY guest_id
                        ) AS payments ON guests.guest_id = payments.guest_id
                        
                        GROUP BY guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, guests.visit_count
                        {search_input_query}
                        """

        elif show_type == "Active Guests":

            sql = f"""SELECT guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, 
                        guests.visit_count, 
                        CAST(COALESCE(reservations.total_cost, 0) -  COALESCE(payments.total_paid, 0) AS SIGNED) AS remaining_balance
                        FROM guests
                        
                        LEFT JOIN (
                            SELECT guest_id, SUM(total_reservation_cost) AS total_cost
                            FROM reservedrooms
                            WHERE reservation_status IN ('Pending', 'Confirmed')
                            GROUP BY guest_id
                        ) AS reservations ON guests.guest_id = reservations.guest_id
                        
                        LEFT JOIN (
                            SELECT guest_id, SUM(amount) AS total_paid
                            FROM paidrooms
                            GROUP BY guest_id
                        ) AS payments ON guests.guest_id = payments.guest_id
                        
                        WHERE guests.guest_id IN (
                            SELECT guest_id FROM reservedrooms WHERE reservation_status = 'Pending'
                            UNION
                            SELECT guest_id FROM bookedrooms WHERE check_in_status = 'In Progress'
                        )
                        
                        GROUP BY guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, guests.visit_count
                        {search_input_query}
                        """

        else:
            sql = f"""SELECT guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, 
                        guests.visit_count, 
                        CAST(COALESCE(reservations.total_cost, 0) -  COALESCE(payments.total_paid, 0) AS SIGNED) AS remaining_balance
                        FROM guests
                        
                        LEFT JOIN (
                            SELECT guest_id, SUM(total_reservation_cost) AS total_cost
                            FROM reservedrooms
                            WHERE reservation_status IN ('Pending', 'Confirmed')
                            GROUP BY guest_id
                        ) AS reservations ON guests.guest_id = reservations.guest_id
                        
                        LEFT JOIN (
                            SELECT guest_id, SUM(amount) AS total_paid
                            FROM paidrooms
                            GROUP BY guest_id
                        ) AS payments ON guests.guest_id = payments.guest_id
                        
                        GROUP BY guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, guests.visit_count
                        {search_input_query}
                        """

        if sort_by == "Total Amount Due":
            sql += f" ORDER BY remaining_balance"
        else:
            sql += f" ORDER BY guests.{guest_table_columns[sort_by]}"

        sql += f""" {sort_type_formatted[sort_type]}, guests.name ASC 
                    LIMIT {max_guests_per_page} 
                    OFFSET {max_guests_per_page * (current_page_number - 1)}"""

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_guest_count(self, show_type=None,  search_input=None):

        if search_input and show_type == "All Guests":
            search_input_query = """ HAVING
                      guests.name LIKE %s OR
                      guests.phone_number LIKE %s OR
                      guests.last_visit_date LIKE %s OR
                      CAST(guests.visit_count AS CHAR) LIKE %s OR
                      CAST(COALESCE(SUM(reservedrooms.total_reservation_cost), 0) - COALESCE(SUM(paidrooms.amount), 0) AS CHAR) LIKE %s"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input)
        elif search_input:
            search_input_query = """ HAVING
                                  guests.name LIKE %s OR
                                  guests.phone_number LIKE %s OR
                                  guests.last_visit_date LIKE %s OR
                                  CAST(guests.visit_count AS CHAR) LIKE %s OR
                                  CAST(COALESCE(reservations.total_cost, 0) - COALESCE(payments.total_paid, 0) AS CHAR) LIKE %s"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input, search_input, search_input, search_input)
        else:
            search_input_query = ""
            values = ()

        if show_type == "With Reservations":

            sql = f"""SELECT COUNT(*) FROM (
                        SELECT guests.guest_id FROM guests

                        LEFT JOIN (
                            SELECT guest_id, SUM(total_reservation_cost) AS total_cost
                            FROM reservedrooms
                            WHERE reservation_status IN ('pending', 'confirmed')
                            GROUP BY guest_id
                        ) AS reservations ON guests.guest_id = reservations.guest_id

                        LEFT JOIN (
                            SELECT guest_id, SUM(amount) AS total_paid
                            FROM paidrooms
                            GROUP BY guest_id
                        ) AS payments ON guests.guest_id = payments.guest_id

                        WHERE guests.guest_id IN (
                            SELECT guest_id FROM reservedrooms WHERE reservation_status = 'pending'
                        )

                        GROUP BY guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, guests.visit_count

                        {search_input_query}
                    ) AS filtered_guests;
                        """

        elif show_type == "Currently Staying":

            sql = f"""SELECT COUNT(*) FROM (
                        SELECT guests.guest_id FROM guests

                        LEFT JOIN (
                            SELECT guest_id, SUM(total_reservation_cost) AS total_cost
                            FROM reservedrooms
                            WHERE reservation_status IN ('pending', 'confirmed')
                            GROUP BY guest_id
                        ) AS reservations ON guests.guest_id = reservations.guest_id

                        LEFT JOIN (
                            SELECT guest_id, SUM(amount) AS total_paid
                            FROM paidrooms
                            GROUP BY guest_id
                        ) AS payments ON guests.guest_id = payments.guest_id

                        WHERE guests.guest_id IN (
                            SELECT guest_id FROM bookedrooms WHERE check_in_status = 'in progress'
                        )

                        GROUP BY guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, guests.visit_count

                        {search_input_query}
                    ) AS filtered_guests;
                        """

        elif show_type == "Active Guests":

            sql = f"""SELECT COUNT(*) FROM (
                        SELECT guests.guest_id FROM guests

                        LEFT JOIN (
                            SELECT guest_id, SUM(total_reservation_cost) AS total_cost
                            FROM reservedrooms
                            WHERE reservation_status IN ('pending', 'confirmed')
                            GROUP BY guest_id
                        ) AS reservations ON guests.guest_id = reservations.guest_id

                        LEFT JOIN (
                            SELECT guest_id, SUM(amount) AS total_paid
                            FROM paidrooms
                            GROUP BY guest_id
                        ) AS payments ON guests.guest_id = payments.guest_id

                        WHERE guests.guest_id IN (
                            SELECT guest_id FROM reservedrooms WHERE reservation_status = 'pending'
                            UNION
                            SELECT guest_id FROM bookedrooms WHERE check_in_status = 'in progress'
                        )

                        GROUP BY guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, guests.visit_count

                        {search_input_query}
                    ) AS filtered_guests;
                    """

        else:
            sql = f"""SELECT COUNT(*) FROM (
                        SELECT guests.guest_id
                        FROM guests
                        LEFT JOIN reservedrooms ON guests.guest_id = reservedrooms.guest_id 
                        LEFT JOIN paidrooms ON guests.guest_id = paidrooms.guest_id
                        GROUP BY guests.guest_id, guests.name, guests.phone_number, guests.last_visit_date, guests.visit_count
                        {search_input_query}
                    ) AS filtered_guests;
                        """

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()[0]

        return result

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

        sql = f"""SELECT guests.guest_id, guests.name, guests.gender, guests.home_address, 
                        guests.email_address, guests.phone_number, guests.birth_date,
                        guests.government_id, guests.last_visit_date, guests.visit_count,
                        CAST(COALESCE(reservations.total_cost, 0) -  COALESCE(payments.total_paid, 0) AS SIGNED) AS remaining_balance
                        FROM guests
                        
                        LEFT JOIN (
                            SELECT guest_id, SUM(total_reservation_cost) AS total_cost
                            FROM reservedrooms
                            GROUP BY guest_id
                        ) AS reservations ON guests.guest_id = reservations.guest_id
                        
                        LEFT JOIN (
                            SELECT guest_id, SUM(amount) AS total_paid
                            FROM paidrooms
                            GROUP BY guest_id
                        ) AS payments ON guests.guest_id = payments.guest_id
                        
                        
                        WHERE guests.guest_id=%s;"""

        values = (guest_id,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result[0]

    def get_name_from_guest_id(self, guest_id):
        sql = f"""SELECT guests.name
                            FROM guests
                            WHERE guests.guest_id=%s;"""

        values = (guest_id,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0]

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
                (guest_id, name, gender, home_address, email_address, phone_number, 
                birth_date, government_id, visit_count) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        # sql = """INSERT INTO guests
        #                 (guest_id, name, sex, home_address, email_address, phone_number,
        #                 birth_date, government_id, visit_count) VALUES
        #                 (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        #                 ON DUPLICATE KEY UPDATE name = name"""

        latest_guest_id = self.get_latest_guest_id()

        new_guest_id = f"guest-{int(latest_guest_id[7:]) + 1:06}"

        values = (new_guest_id,
                  guest_information["name"],
                  guest_information["gender"],
                  guest_information["home_address"],
                  guest_information["email_address"],
                  guest_information["phone_number"],
                  guest_information["birth_date"],
                  guest_information["government_id"],
                  0)

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_guest(self, old_guest_id, guest_information):
        sql = """UPDATE guests 
                SET name=%s, gender=%s, home_address=%s, email_address=%s, phone_number=%s, 
                birth_date=%s, government_id=%s WHERE 
                guest_id=%s"""

        values = (guest_information['name'],
                  guest_information['gender'],
                  guest_information['home_address'],
                  guest_information['email_address'],
                  guest_information['phone_number'],
                  guest_information['birth_date'],
                  guest_information['government_id'],
                  old_guest_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    # def delete_guest(self, identifier_type, identifier):
    #
    #     sql = ""
    #     values = (identifier.strip(),)
    #
    #     if identifier_type == "guest_id":
    #         sql = "DELETE FROM guests WHERE guest_id=%s"
    #     elif identifier_type == "name":
    #         sql = "DELETE FROM guests WHERE name=%s"
    #
    #     self.cursor.execute(sql, values)
    #     self.db.commit()
