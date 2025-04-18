import pymysql
from dotenv import load_dotenv
import os

from database_driver.initialize_database import InitializeDatabase


load_dotenv()


class DatabaseDriver:

    def __init__(self):

        self.check_environment_variables()

        self.db = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database='hms_db'
        )

        self.cursor = self.db.cursor()

        InitializeDatabase(self.cursor)

    def get_latest_guest_id(self):

        self.cursor.execute("""SELECT guest_id FROM guests
            ORDER BY CAST(SUBSTRING(guest_id, 7) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "guest-000000"
        else:
            return result[0]

    def add_guest(self, guest_information):
        sql = """INSERT INTO guests 
                (guest_id, name, sex, home_address, email_address, phone_number, 
                birth_date, government_id, visit_count) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        latest_guest_id = self.get_latest_guest_id()

        new_guest_id = f"guest-{int(latest_guest_id[7:]) + 1:06}"

        values = (new_guest_id,
                  guest_information[0],
                  guest_information[1],
                  guest_information[2],
                  guest_information[3],
                  guest_information[4],
                  guest_information[5],
                  guest_information[6],
                  1)

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_guest(self, old_guest_id, guest_information):
        sql = """UPDATE guests 
                SET guest_id=%s, name=%s, sex=%s, home_address=%s, email_address=%s, phone_number=%s, 
                birth_date=%s, government_id=%s, last_visit_date=%s, visit_count=%s WHERE 
                guest_id=%s"""

        values = (guest_information[0],
                  guest_information[1],
                  guest_information[2],
                  guest_information[3],
                  guest_information[4],
                  guest_information[5],
                  guest_information[6],
                  guest_information[7],
                  guest_information[8],
                  guest_information[9],
                  old_guest_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_guest(self, identifier_type, identifier):

        sql = ""
        values = (identifier.strip(),)

        if identifier_type == "guest_id":
            sql = "DELETE FROM guests WHERE guest_id=%s"
        elif identifier_type == "name":
            sql = "DELETE FROM guests WHERE name=%s"

        self.cursor.execute(sql, values)
        self.db.commit()



    def check_environment_variables(self):
        if not all([os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD")]):
            raise EnvironmentError("Missing one or more required DB environment variables.")
