from models.recent_stays_model import RecentStaysModel
from models.reservation_model import ReservationModel


class DashboardController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.load_data()

    def load_data(self):
        self.set_models()



    def set_models(self):
        recent_check_in_initial_data = self.db_driver.get_all_booked_room_today("check_in")
        recent_check_out_initial_data = self.db_driver.get_all_booked_room_today("check_out")
        reservations_initial_data = self.db_driver.get_all_reservations()

        self.recent_check_in_table_model = RecentStaysModel(recent_check_in_initial_data)
        self.recent_check_out_table_model = RecentStaysModel(recent_check_out_initial_data)
        self.reservation_table_model = ReservationModel(reservations_initial_data)

        self.view.recent_check_in_frame_table_view.setModel(self.recent_check_in_table_model)
        self.view.recent_check_out_frame_table_view.setModel(self.recent_check_out_table_model)
        self.view.reservation_list_frame_table_view.setModel(self.reservation_table_model)

