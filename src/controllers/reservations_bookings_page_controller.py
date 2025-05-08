from models import ReservationModel


class ReservationsBookingsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.set_models()

        self.view.set_table_views_column_widths()

    def connect_signals_to_slots(self):
        pass

    def set_models(self):
        reservations_initial_data = self.db_driver.reserved_room_queries.get_all_reservations()

        self.reservation_table_model = ReservationModel(reservations_initial_data, "reservation_page_view")

        self.view.reservations_table_view.setModel(self.reservation_table_model)

