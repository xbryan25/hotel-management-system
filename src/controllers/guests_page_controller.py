from models.guests_model import GuestsModel


class GuestsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget

        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.set_models()
        self.view.set_table_views_column_widths()

    def set_models(self):

        sort_by_text = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        sort_type_text = self.view.sort_type_combobox.currentText()

        guests_data_from_db = self.db_driver.get_active_guests(sort_by_text, sort_type_text)

        self.guests_model = GuestsModel(guests_data_from_db)

        self.view.guest_table_view.setModel(self.guests_model)

    def connect_signals_to_slots(self):
        self.view.sort_by_combobox.currentTextChanged.connect(self.update_guests_table_view)
        self.view.sort_type_combobox.currentTextChanged.connect(self.update_guests_table_view)

    def update_guests_table_view(self):
        sort_by_text = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        sort_type_text = self.view.sort_type_combobox.currentText()

        guests_data_from_db = self.db_driver.get_active_guests(sort_by_text, sort_type_text)

        self.guests_model.update_data(guests_data_from_db)
