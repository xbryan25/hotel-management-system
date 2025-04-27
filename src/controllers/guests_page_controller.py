from models.guests_model import GuestsModel


class GuestsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget

        self.db_driver = db_driver

        self.set_models()
        self.view.set_table_views_column_widths()

    def set_models(self):
        guests_data_from_db = self.db_driver.get_active_guests()

        self.guests_model = GuestsModel(guests_data_from_db)

        self.view.guest_table_view.setModel(self.guests_model)
