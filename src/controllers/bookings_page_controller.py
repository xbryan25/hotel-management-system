from datetime import datetime

from models import BookingModel

from views import BookingInfoDialog, ConfirmationDialog, FeedbackDialog
from controllers.booking_info_dialog_controller import BookingInfoDialogController


class BookingsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.bookings_model = None

        self.prev_view_type = None
        self.prev_sort_by = None
        self.prev_sort_type = None
        self.prev_search_input = None

        self.current_page_number = 1
        self.max_bookings_per_page = 16

    def set_page_number_lineedit_validator(self, total_pages):
        self.view.set_page_number_lineedit_validator(total_pages)

    def open_booking_info_dialog(self, index):
        selected_booking_id = index.sibling(index.row(), 0).data()

        self.booking_info_dialog = BookingInfoDialog()
        self.booking_info_dialog_controller = BookingInfoDialogController(self.booking_info_dialog,
                                                                          self.db_driver,
                                                                          selected_booking_id)

        self.booking_info_dialog.exec()

        # self.refresh_reservations_data()

    def connect_signals_to_slots(self):
        self.view.window_resized.connect(self.update_row_count)

        self.view.sort_by_combobox.currentTextChanged.connect(self.refresh_bookings_data)
        self.view.sort_type_combobox.currentTextChanged.connect(self.refresh_bookings_data)
        self.view.view_type_combobox.currentTextChanged.connect(self.refresh_bookings_data)

        self.view.clicked_info_button.connect(self.open_booking_info_dialog)
        self.view.clicked_check_out_button.connect(self.booking_check_out)

        self.view.search_text_changed.connect(self.update_prev_search_input)
        self.view.search_text_changed.connect(lambda _: self.refresh_bookings_data())

        self.view.next_page_button_pressed.connect(self.go_to_next_page)
        self.view.previous_page_button_pressed.connect(self.go_to_previous_page)

        self.view.page_number_lineedit_changed.connect(self.change_page_number_lineedit)

    def change_page_number_lineedit(self, page_number):

        booking_count = self.db_driver.booked_room_queries.get_booking_count(view_type=self.prev_view_type,
                                                                             search_input=self.prev_search_input)
        total_pages = max(self.total_pages(booking_count), 1)

        if not page_number:
            self.current_page = 1
        elif int(page_number) < 1:
            self.current_page = 1
            self.view.page_number_lineedit.setText(str(self.current_page))
        elif int(page_number) > total_pages:
            self.current_page = total_pages
            self.view.page_number_lineedit.setText(str(self.current_page))
        else:
            self.current_page = int(page_number)

        self.refresh_bookings_data()

    def booking_check_out(self, index):

        selected_booking_id = index.sibling(index.row(), 0).data()
        # booking_room_number = index.sibling(index.row(), 2).data()

        self.confirmation_dialog = ConfirmationDialog(f"Confirm check-out of {selected_booking_id}?")

        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_choice():

            self.db_driver.booked_room_queries.set_check_out_booking(selected_booking_id)
            # self.db_driver.room_queries.set_room_status(booking_room_number, 'available')

            self.refresh_bookings_data()

            self.feedback_dialog = FeedbackDialog("Success!", f"{selected_booking_id} has checked out successfully")
            self.feedback_dialog.exec()

    def update_row_count(self):
        current_max_bookings_per_page = self.view.get_max_rows_of_bookings_table_view()

        if current_max_bookings_per_page != 0 and self.max_bookings_per_page != current_max_bookings_per_page:

            self.max_bookings_per_page = current_max_bookings_per_page

            self.view.bookings_table_view.setUpdatesEnabled(False)
            self.refresh_bookings_data()
            self.view.bookings_table_view.setUpdatesEnabled(True)
            self.view.bookings_table_view.viewport().update()


    def update_prev_search_input(self, search_input):
        self.prev_search_input = search_input

    def go_to_next_page(self):
        booking_count = self.db_driver.booked_room_queries.get_booking_count(view_type=self.prev_view_type,
                                                                             search_input=self.prev_search_input)

        if self.current_page_number + 1 <= self.total_pages(booking_count):
            self.current_page_number += 1

            self.view.page_number_lineedit.setText(str(self.current_page))

            self.refresh_bookings_data()

    def go_to_previous_page(self):
        if self.current_page_number > 1:
            self.current_page_number -= 1

            self.view.page_number_lineedit.setText(str(self.current_page))

            self.refresh_bookings_data()

    def total_pages(self, booking_count):
        return (booking_count + self.max_bookings_per_page - 1) // self.max_bookings_per_page

    def refresh_bookings_data(self):
        self.prev_view_type = self.view.view_type_combobox.currentText()
        self.prev_sort_by = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        self.prev_sort_type = self.view.sort_type_combobox.currentText()

        self.set_models()

        self.check_if_underflow_contents()

    def check_if_underflow_contents(self):
        if self.bookings_model.get_len_of_data() == 0:
            self.go_to_previous_page()

    def set_models(self):
        bookings_data_from_db = self.db_driver.booked_room_queries.get_all_bookings(max_bookings_per_page=self.max_bookings_per_page,
                                                                                    current_page_number=self.current_page_number,
                                                                                    view_type=self.prev_view_type,
                                                                                    sort_by=self.prev_sort_by,
                                                                                    sort_type=self.prev_sort_type,
                                                                                    search_input=self.prev_search_input)

        if not self.bookings_model:
            self.bookings_model = BookingModel(bookings_data_from_db)
            self.view.bookings_table_view.setModel(self.bookings_model)
            self.view.set_table_views_column_widths()
        else:
            self.bookings_model.update_data(bookings_data_from_db)

        booking_count = self.db_driver.booked_room_queries.get_booking_count(view_type=self.prev_view_type,
                                                                             search_input=self.prev_search_input)

        self.set_page_number_lineedit_validator(self.total_pages(booking_count))
        self.view.update_of_page_number_label(self.total_pages(booking_count))

