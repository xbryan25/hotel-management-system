from datetime import datetime

from models import BookingModel
from views.message_dialogs import ConfirmationDialog, FeedbackDialog


class BookingsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.set_models()

        self.view.set_table_views_column_widths()

    def connect_signals_to_slots(self):
        self.view.sort_by_combobox.currentTextChanged.connect(self.update_bookings_table_view)
        self.view.sort_type_combobox.currentTextChanged.connect(self.update_bookings_table_view)
        self.view.view_type_combobox.currentTextChanged.connect(self.update_bookings_table_view)

        self.view.clicked_info_button.connect(lambda: print("clicked info button"))
        self.view.clicked_check_out_button.connect(self.booking_check_out)

    def booking_check_out(self, index):

        selected_booking_id = index.sibling(index.row(), 0).data()
        booking_room_number = index.sibling(index.row(), 2).data()

        self.confirmation_dialog = ConfirmationDialog(f"Confirm check-out of {selected_booking_id}?")

        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_choice():

            self.db_driver.booked_room_queries.set_check_out_booking(selected_booking_id)
            self.db_driver.room_queries.set_room_status(booking_room_number, 'available')

            self.update_bookings_table_view()

            self.feedback_dialog = FeedbackDialog("Success!", f"{selected_booking_id} has checked out successfully")
            self.feedback_dialog.exec()

    def set_models(self):
        bookings_initial_data = self.db_driver.booked_room_queries.get_all_bookings()

        self.booking_table_model = BookingModel(bookings_initial_data)

        self.view.bookings_table_view.setModel(self.booking_table_model)

    def update_bookings_table_view(self):
        sort_by_text = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        sort_type_text = self.view.sort_type_combobox.currentText()
        view_type_text = self.view.view_type_combobox.currentText()

        bookings_data_from_db = self.db_driver.booked_room_queries.get_all_bookings(sort_by=sort_by_text,
                                                                                    sort_type=sort_type_text,
                                                                                    view_type=view_type_text)

        self.booking_table_model.update_data(bookings_data_from_db)
