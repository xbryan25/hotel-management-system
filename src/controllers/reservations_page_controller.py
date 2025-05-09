from models import ReservationModel


class ReservationsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.set_models()

        self.view.set_table_views_column_widths()

    def connect_signals_to_slots(self):
        self.view.sort_by_combobox.currentTextChanged.connect(self.update_reservations_table_view)
        self.view.sort_type_combobox.currentTextChanged.connect(self.update_reservations_table_view)
        self.view.view_type_combobox.currentTextChanged.connect(self.update_reservations_table_view)

    def set_models(self):
        reservations_initial_data = self.db_driver.reserved_room_queries.get_all_reservations()

        self.reservation_table_model = ReservationModel(reservations_initial_data, "reservation_page_view")

        self.view.reservations_table_view.setModel(self.reservation_table_model)

    def update_reservations_table_view(self):
        sort_by_text = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        sort_type_text = self.view.sort_type_combobox.currentText()
        view_type_text = self.view.view_type_combobox.currentText()

        reservations_data_from_db = self.db_driver.reserved_room_queries.get_all_reservations(sort_by=sort_by_text,
                                                                                              sort_type=sort_type_text,
                                                                                              view_type=view_type_text)

        self.reservation_table_model.update_data(reservations_data_from_db)
