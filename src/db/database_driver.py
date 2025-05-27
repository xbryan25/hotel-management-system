import pymysql
from datetime import date

from dotenv import load_dotenv
import os

from db.initialize_database import InitializeDatabase
from db.queries import *

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
        self.cursor.execute("SET SQL_SAFE_UPDATES = 0;")

        self.init_db = InitializeDatabase(self.cursor)

        self.availed_service_queries = AvailedServiceQueries(self.db, self.cursor)
        self.booked_room_queries = BookedRoomQueries(self.db, self.cursor)
        self.guest_queries = GuestQueries(self.db, self.cursor)
        self.paid_room_queries = PaidRoomQueries(self.db, self.cursor)
        self.reserved_room_queries = ReservedRoomQueries(self.db, self.cursor)
        self.room_queries = RoomQueries(self.db, self.cursor)
        self.service_queries = ServiceQueries(self.db, self.cursor)

    def close_connection(self):
        self.cursor.execute("SET SQL_SAFE_UPDATES = 1;")
        self.db.close()

    @staticmethod
    def check_environment_variables():
        if not all([os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD")]):
            raise EnvironmentError("Missing one or more required DB environment variables.")
