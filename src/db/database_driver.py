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

        self.init_db = InitializeDatabase(self.cursor)

        self.availed_service_queries = AvailedServiceQueries(self.cursor)
        self.booked_room_queries = BookedRoomQueries(self.cursor)
        self.guest_queries = GuestQueries(self.cursor)
        self.paid_room_queries = PaidRoomQueries(self.cursor)
        self.reserved_room_queries =  ReservedRoomQueries(self.cursor)
        self.room_queries = RoomQueries(self.cursor)
        self.service_queries = ServiceQueries(self.cursor)

    def close_connection(self):
        self.db.close()

    @staticmethod
    def check_environment_variables():
        if not all([os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD")]):
            raise EnvironmentError("Missing one or more required DB environment variables.")
