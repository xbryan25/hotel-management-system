from models import GuestsModel, GuestInfoModel
from views import GuestInfoDialog


class GuestsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget

        self.db_driver = db_driver

        self.current_guest_model = None
        self.guests_model = None
        self.guest_info_dialog = GuestInfoDialog()

        self.connect_signals_to_slots()

        # self.set_models()


        self.prev_sort_by = None
        self.prev_sort_type = None
        self.prev_search_input = None

        self.current_page_number = 1
        self.max_guests_per_page = 50

    def set_models(self):

        guests_data_from_db = self.db_driver.guest_queries.get_all_guests(max_guests_per_page=self.max_guests_per_page,
                                                                          current_page_number=self.current_page_number,
                                                                          sort_by=self.prev_sort_by,
                                                                          sort_type=self.prev_sort_type,
                                                                          search_input=self.prev_search_input)

        if not self.guests_model:
            self.guests_model = GuestsModel(guests_data_from_db)
            self.view.guest_table_view.setModel(self.guests_model)
            self.view.guest_table_view.hide_first_column()
            self.view.set_table_views_column_widths()
        else:
            self.guests_model.update_data(guests_data_from_db)

    def connect_signals_to_slots(self):
        self.view.sort_by_combobox.currentTextChanged.connect(self.refresh_guests_data)
        self.view.sort_type_combobox.currentTextChanged.connect(self.refresh_guests_data)

        self.view.clicked_info_button.connect(self.show_guest_info)

        self.guest_info_dialog.mode_changed.connect(self.switch_information_mode_guest_info)

        self.view.search_text_changed.connect(self.update_prev_search_input)
        self.view.search_text_changed.connect(lambda _: self.refresh_guests_data())

    def update_prev_search_input(self, search_input):
        self.prev_search_input = search_input

    def go_to_next_page(self):
        room_count = 10
        # room_count = self.db_driver.room_queries.get_guest_count("all", search_input=self.prev_search_input)

        if self.current_page_number + 1 <= self.total_pages(room_count):
            self.current_page_number += 1

            self.refresh_guests_data()

    def go_to_previous_page(self):

        if self.current_page_number > 1:
            self.current_page_number -= 1
            self.refresh_guests_data()

    def total_pages(self, room_count):
        return (room_count + self.max_rows_per_page - 1) // self.max_rows_per_page

    def refresh_guests_data(self):
        self.prev_sort_by = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        self.prev_sort_type = self.view.sort_type_combobox.currentText()

        self.set_models()

    def check_if_underflow_contents(self):
        if self.guests_model.get_len_of_data() == 0:
            self.go_to_previous_page()
            return True

        return False

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

