import pymysql

from database_driver.initialize_database import InitializeDatabase


class DatabaseDriver:

    def __init__(self):

        db_initial_user_values = ["root", "root"]

        input_user = input("Input user (default: root): ")
        input_password = input("Input password (default: root): ")

        if input_user.strip() != "":
            db_initial_user_values[0] = input_user

        if input_password.strip() != "":
            db_initial_user_values[1] = input_password

        self.db = pymysql.connect(
            host='localhost',
            user=db_initial_user_values[0],
            password=db_initial_user_values[1],
            database='hms_db'
        )

        self.cursor = self.db.cursor()

        InitializeDatabase(self.cursor)



