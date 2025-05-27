from datetime import datetime


class AvailedServiceQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def refresh_availed_services(self):
        # self.cursor.execute("SET SQL_SAFE_UPDATES = 0;")

        sql_r = """UPDATE availedservices
                    JOIN reservedrooms ON availedservices.avail_date = reservedrooms.last_modified
                    SET availedservices.avail_status = %s
                    WHERE availedservices.avail_status = %s
                        AND reservedrooms.reservation_status IN ('Cancelled', 'Expired');
                """

        values_r = ('Cancelled', 'Active')

        self.cursor.execute(sql_r, values_r)

        sql_b = """UPDATE availedservices
                    JOIN reservedrooms ON availedservices.avail_date = reservedrooms.last_modified 
                        AND reservedrooms.reservation_status = %s
                    JOIN bookedrooms ON
                        reservedrooms.check_in_date = bookedrooms.check_in_date AND reservedrooms.check_out_date = bookedrooms.check_out_date AND
                        reservedrooms.guest_id = bookedrooms.guest_id AND reservedrooms.room_id = bookedrooms.room_id
                    SET availedservices.avail_status = %s
                    WHERE availedservices.avail_status=%s AND bookedrooms.check_in_status=%s;
                """

        values_b = ('Confirmed', 'Completed', 'Active', 'Finished')

        self.cursor.execute(sql_b, values_b)

        # self.cursor.execute("SET SQL_SAFE_UPDATES = 1;")

        self.db.commit()

    def get_count_of_most_availed_services(self, view_type='Today'):

        sql = """SELECT services.service_name, COUNT(*) AS cnt FROM availedservices
                    JOIN services ON availedservices.service_id=services.service_id
                    """

        if view_type == 'Today':
            sql += """WHERE DATE(availedservices.avail_date) = CURDATE() """

        elif view_type == 'This Week':
            sql += """WHERE YEARWEEK(availedservices.avail_date, 1) = YEARWEEK(CURDATE(), 1) """

        elif view_type == 'This Month':
            sql += """WHERE MONTH(availedservices.avail_date) = MONTH(CURDATE())
                        AND YEAR(availedservices.avail_date) = YEAR(CURDATE()) """

        elif view_type == 'This Year':
            sql += """WHERE YEAR(availedservices.avail_date) = YEAR(CURDATE()) """

        sql += """AND avail_status='Active' AND services.is_active=1 
                    GROUP BY services.service_name ORDER BY cnt DESC LIMIT 5;"""

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result

    def get_availed_services_from_avail_date(self, avail_date):
        sql = f"""SELECT services.service_id, services.service_name, availedservices.quantity, services.rate, 
                    availedservices.avail_id
                    FROM availedservices
                    LEFT JOIN services ON availedservices.service_id = services.service_id
                    WHERE avail_date=%s AND avail_status=%s"""

        values = (avail_date, 'Active')

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_latest_avail_id(self):

        self.cursor.execute("""SELECT avail_id FROM availedservices
            ORDER BY CAST(SUBSTRING(avail_id, 7) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "avail-000000"
        else:
            return result[0]

    def add_availed_services(self, availed_service_information, guest_id, date_time_now=None):

        if not date_time_now:
            date_time_now = datetime.now()

        for service_id, quantity in availed_service_information.items():

            sql = """INSERT INTO availedservices
                    (avail_id, avail_date, avail_status, quantity, guest_id, service_id) VALUES
                    (%s, %s, %s, %s, %s, %s)"""

            latest_avail_id = self.get_latest_avail_id()

            new_avail_id = f"avail-{int(latest_avail_id[9:]) + 1:06}"

            values = (new_avail_id,
                      date_time_now,
                      'Active',
                      quantity,
                      guest_id,
                      service_id)

            self.cursor.execute(sql, values)
            self.db.commit()

    def update_availed_services(self, availed_service_information, date_time_now=None):

        if not date_time_now:
            date_time_now = datetime.now()

        for avail_id, avail_information in availed_service_information.items():

            sql = """UPDATE availedservices SET avail_date=%s, quantity=%s, avail_status=%s WHERE avail_id=%s"""

            values = (date_time_now, avail_information['quantity'], avail_information['avail_status'], avail_id)

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
