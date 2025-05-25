

class ServiceQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def get_service_id_from_service_name(self, service_name):
        sql = "SELECT services.service_id FROM services WHERE service_name=%s;"
        values = (service_name,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_service_details(self, service_id):
        sql = "SELECT * FROM services WHERE service_id=%s;"
        values = (service_id,)

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()

        return result if result else None

    def set_service_active_status(self, is_active, service_id):
        sql = "UPDATE services SET is_active=%s WHERE service_id=%s"
        values = (is_active, service_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def get_service_active_status(self, service_id):
        sql = "SELECT services.is_active FROM services WHERE service_id = %s;"
        values = (service_id,)

        self.cursor.execute(sql, values)
        result = self.cursor.fetchone()[0]

        return True if result == 1 else False

    def does_service_name_exist(self, service_name):
        sql = "SELECT 1 FROM services WHERE service_name = %s LIMIT 1;"
        values = (service_name,)

        self.cursor.execute(sql, values)
        result = self.cursor.fetchone()

        return result[0] if result else None

    def get_latest_service_id(self):

        self.cursor.execute("""SELECT service_id FROM services
            ORDER BY CAST(SUBSTRING(service_id, 9) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "service-000"
        else:
            return result[0]

    def get_all_services(self, enable_pagination=False, max_services_per_page=20, current_page=1,
                         view_type="Active Services", sort_by="Service Name", sort_type="Ascending",
                         search_input=None):

        sort_by_dict = {"Service Name": "services.service_name",
                        "Rate": "services.rate"}

        sort_type_dict = {"Ascending": "ASC", "Descending": "DESC"}

        view_type_dict = {"Active Services": "WHERE services.is_active = 1",
                          "Inactive Services": "WHERE services.is_active = 0",
                          "All": ""}

        if search_input and view_type_dict in ('Active Services', 'Inactive Services'):
            search_input_query = """ AND 
                                (services.service_name LIKE %s OR 
                                services.rate LIKE %s)"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input)
        elif search_input and view_type_dict == "All":
            search_input_query = """ WHERE
                                    (services.service_name LIKE %s OR 
                                    services.rate LIKE %s)"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input)

        else:
            search_input_query = ""
            values = ()

        sql = f"""SELECT services.service_id, services.service_name, services.rate, services.is_active
                FROM services
                {view_type_dict[view_type]}
                {search_input_query}
                ORDER BY {sort_by_dict[sort_by]} {sort_type_dict[sort_type]}"""

        if enable_pagination:
            sql += f""" LIMIT {max_services_per_page} OFFSET {max_services_per_page * (current_page - 1)}"""

        self.cursor.execute(sql, values)

        result = self.cursor.fetchall()

        list_result = [list(row) for row in result]

        return list_result

    def get_service_count(self, view_type=None, search_input=None):

        view_type_dict = {"Active Services": "WHERE services.is_active = 1",
                          "Inactive Services": "WHERE services.is_active = 0",
                          "All": ""}

        if search_input and view_type_dict in ('Active Services', 'Inactive Services'):
            search_input_query = """ AND 
                                        (services.service_name LIKE %s OR 
                                        services.rate LIKE %s)"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input)

        elif search_input and view_type_dict == "All":
            search_input_query = """ WHERE
                                    (services.service_name LIKE %s OR 
                                    services.rate LIKE %s)"""

            search_input = f"%{search_input}%"
            values = (search_input, search_input)

        else:
            search_input_query = ""
            values = ()

        sql = f"""SELECT COUNT(*)
                        FROM services
                        {view_type_dict[view_type]}
                        {search_input_query}"""

        self.cursor.execute(sql, values)

        result = self.cursor.fetchone()[0]

        return result

    def add_service(self, service_information):
        sql = """INSERT INTO services
                (service_id, service_name, rate, is_active) VALUES
                (%s, %s, %s, %s)"""

        latest_service_id = self.get_latest_service_id()

        new_service_id = f"service-{int(latest_service_id[9:]) + 1:03}"

        values = (new_service_id,
                  service_information['service_name'],
                  service_information['rate'],
                  True)

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_service(self, service_id, service_inputs):
        sql = """UPDATE services SET service_name=%s, rate=%s WHERE service_id=%s;"""

        values = (service_inputs['service_name'],
                  service_inputs['rate'],
                  service_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_service(self, identifier):

        sql = "DELETE FROM services WHERE service_id=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()