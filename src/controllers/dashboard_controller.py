from models.recent_stays_model import RecentStaysModel
from models.reservation_model import ReservationModel


class DashboardController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.set_models()

    def set_models(self):
        self.view.recent_check_in_frame_table_view.setModel(RecentStaysModel())
        self.view.recent_check_out_frame_table_view.setModel(RecentStaysModel())
        self.view.reservation_list_frame_table_view.setModel(ReservationModel())
