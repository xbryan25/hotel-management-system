from models import GuestsModel, GuestInfoModel
from views import GuestInfoDialog


class GuestsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget

        self.db_driver = db_driver

        self.current_guest_model = None
        self.guest_info_dialog = GuestInfoDialog()

        self.connect_signals_to_slots()

        self.set_models()
        self.view.set_table_views_column_widths()

    def set_models(self):

        sort_by_text = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        sort_type_text = self.view.sort_type_combobox.currentText()

        guests_data_from_db = self.db_driver.guest_queries.get_active_guests(sort_by_text, sort_type_text)

        self.guests_model = GuestsModel(guests_data_from_db)

        self.view.guest_table_view.setModel(self.guests_model)
        self.view.guest_table_view.hide_first_column()

    def connect_signals_to_slots(self):
        self.view.sort_by_combobox.currentTextChanged.connect(self.update_guests_table_view)
        self.view.sort_type_combobox.currentTextChanged.connect(self.update_guests_table_view)

        self.view.clicked_info_button.connect(self.show_guest_info)

        self.guest_info_dialog.mode_changed.connect(self.switch_information_mode_guest_info)

    def show_guest_info(self, index):
        # Get guest_id of guest from index
        guest_id = self.guests_model.get_guest_id(index.row())
        print(guest_id)

        # Load data from db
        # Put fetched data to model
        # Put model data to view

        guest_data = self.db_driver.guest_queries.get_guest_details(guest_id)
        self.current_guest_model = GuestInfoModel.from_list(guest_data)

        self.guest_info_dialog.set_guest_info(self.current_guest_model.to_dict())
        self.guest_info_dialog.exec()

    def switch_information_mode_guest_info(self):
        self.guest_info_dialog.set_guest_info(self.current_guest_model.to_dict())
        # self.guest_info_dialog.exec()

    def update_guests_table_view(self):
        sort_by_text = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        sort_type_text = self.view.sort_type_combobox.currentText()

        guests_data_from_db = self.db_driver.guest_queries.get_active_guests(sort_by_text, sort_type_text)

        self.guests_model.update_data(guests_data_from_db)
