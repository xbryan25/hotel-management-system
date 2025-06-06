from PyQt6.QtCore import QTimer

from models import GuestsModel, GuestInfoModel
from views import GuestInfoDialog
from controllers.guest_info_dialog_controller import GuestInfoDialogController


class GuestsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget

        self.db_driver = db_driver

        self.current_guest_model = None
        self.guests_model = None

        self.connect_signals_to_slots()

        self.prev_show_type = None
        self.prev_sort_by = None
        self.prev_sort_type = None
        self.prev_search_input = None

        self.current_page_number = 1
        self.max_guests_per_page = 16

    def set_page_number_lineedit_validator(self, total_pages):
        self.view.set_page_number_lineedit_validator(total_pages)

    def update_row_count(self):
        current_max_guests_per_page = self.view.get_max_rows_of_guest_table_view()

        if current_max_guests_per_page != 0 and self.max_guests_per_page != current_max_guests_per_page:

            self.max_guests_per_page = current_max_guests_per_page

            self.view.guest_table_view.setUpdatesEnabled(False)
            self.refresh_guests_data()
            self.view.guest_table_view.setUpdatesEnabled(True)
            self.view.guest_table_view.viewport().update()

    def set_models(self):

        self.db_driver.reserved_room_queries.update_expired_reservations()
        self.db_driver.booked_room_queries.update_elapsed_bookings()
        self.db_driver.availed_service_queries.refresh_availed_services()

        guests_data_from_db = self.db_driver.guest_queries.get_all_guests(max_guests_per_page=self.max_guests_per_page,
                                                                          current_page_number=self.current_page_number,
                                                                          show_type=self.prev_show_type,
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

        guest_count = self.db_driver.guest_queries.get_guest_count(show_type=self.prev_show_type,
                                                                   search_input=self.prev_search_input)

        self.set_page_number_lineedit_validator(self.total_pages(guest_count))
        self.view.update_of_page_number_label(self.total_pages(guest_count))

    def connect_signals_to_slots(self):
        self.view.window_resized.connect(self.update_row_count)

        self.view.show_type_combobox.currentTextChanged.connect(self.refresh_guests_data)
        self.view.sort_by_combobox.currentTextChanged.connect(self.refresh_guests_data)
        self.view.sort_type_combobox.currentTextChanged.connect(self.refresh_guests_data)

        self.view.clicked_info_button.connect(self.open_guest_info_dialog)

        # self.guest_info_dialog.mode_changed.connect(self.switch_information_mode_guest_info)

        self.view.search_text_changed.connect(self.update_prev_search_input)
        self.view.search_text_changed.connect(lambda _: self.refresh_guests_data())

        self.view.next_page_button_pressed.connect(self.go_to_next_page)
        self.view.previous_page_button_pressed.connect(self.go_to_previous_page)

        self.view.page_number_lineedit_changed.connect(self.change_page_number_lineedit)

    def change_page_number_lineedit(self, page_number):

        guest_count = self.db_driver.guest_queries.get_guest_count(show_type=self.prev_show_type,
                                                                   search_input=self.prev_search_input)
        total_pages = max(self.total_pages(guest_count), 1)

        if not page_number:
            self.current_page_number = 1
        elif int(page_number) < 1:
            self.current_page_number = 1

            self.view.page_number_lineedit.blockSignals(True)
            self.view.page_number_lineedit.setText(str(self.current_page_number))
            self.view.page_number_lineedit.blockSignals(False)
        elif int(page_number) > total_pages:
            self.current_page_number = total_pages

            self.view.page_number_lineedit.blockSignals(True)
            self.view.page_number_lineedit.setText(str(self.current_page_number))
            self.view.page_number_lineedit.blockSignals(False)
        else:
            self.current_page_number = int(page_number)

        self.refresh_guests_data()

    def update_prev_search_input(self, search_input):
        self.prev_search_input = search_input

    def go_to_next_page(self):
        guest_count = self.db_driver.guest_queries.get_guest_count(show_type=self.prev_show_type,
                                                                   search_input=self.prev_search_input)

        if self.current_page_number + 1 <= self.total_pages(guest_count):
            self.current_page_number += 1

            self.view.page_number_lineedit.blockSignals(True)
            self.view.page_number_lineedit.setText(str(self.current_page_number))
            self.view.page_number_lineedit.blockSignals(False)

            self.refresh_guests_data()

    def go_to_previous_page(self):
        if self.current_page_number > 1:
            self.current_page_number -= 1

            self.view.page_number_lineedit.blockSignals(True)
            self.view.page_number_lineedit.setText(str(self.current_page_number))
            self.view.page_number_lineedit.blockSignals(False)
            self.refresh_guests_data()

    def total_pages(self, guest_count):
        return (guest_count + self.max_guests_per_page - 1) // self.max_guests_per_page

    def refresh_guests_data(self):
        self.prev_show_type = self.view.show_type_combobox.currentText()
        self.prev_sort_by = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        self.prev_sort_type = self.view.sort_type_combobox.currentText()

        self.set_models()

        self.check_if_underflow_contents()

    def check_if_underflow_contents(self):
        if self.guests_model.get_len_of_data() == 0:
            self.go_to_previous_page()

    def open_guest_info_dialog(self, index):
        # Get guest_id of guest from index
        guest_id = self.guests_model.get_guest_id(index.row())
        print(guest_id)

        self.guest_info_dialog = GuestInfoDialog()
        self.guest_info_dialog_controller = GuestInfoDialogController(self.guest_info_dialog,
                                                                      self.db_driver,
                                                                      guest_id)


        self.guest_info_dialog.exec()

        self.refresh_guests_data()

    # def switch_information_mode_guest_info(self):
    #     self.guest_info_dialog.set_guest_info(self.current_guest_model.to_dict())
        # self.guest_info_dialog.exec()

