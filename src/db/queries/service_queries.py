

class ServiceQueries:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_latest_service_id(self):

        self.cursor.execute("""SELECT service_id FROM services
            ORDER BY CAST(SUBSTRING(service_id, 9) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "service-000"
        else:
            return result[0]

    def get_all_services(self):
        self.cursor.execute("""SELECT * FROM services;""")

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def add_service(self, service_information):
        sql = """INSERT INTO services
                (service_id, service_name, rate) VALUES
                (%s, %s, %s)"""

        latest_service_id = self.get_latest_service_id()

        new_service_id = f"service-{int(latest_service_id[9:]) + 1:03}"

        values = (new_service_id,
                  service_information[0],
                  service_information[1])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_service(self, old_service_id, service_information):
        sql = """UPDATE services SET service_id=%s, service_name=%s, rate=%s
        WHERE service_id=%s;"""

        values = (service_information[0],
                  service_information[1],
                  service_information[2],
                  old_service_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_service(self, identifier):

        sql = "DELETE FROM services WHERE service_id=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()