from datetime import date


class AvailedServiceQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

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
