from datetime import datetime

from models import ReservationModel
from views import NewReservationDialog, ReservationInfoDialog
from views.message_dialogs import ConfirmationDialog, FeedbackDialog
from controllers.new_reservation_dialog_controller import NewReservationDialogController
from controllers.reservation_info_dialog_controller import ReservationInfoDialogController


class ReservationsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        # self.set_models()

        # self.view.set_table_views_column_widths()
        self.reservations_model = None

        self.prev_view_type = None
        self.prev_sort_by = None
        self.prev_sort_type = None
        self.prev_search_input = None

        self.current_page_number = 1
        self.max_reservations_per_page = 16

    def open_new_reservation_dialog(self):

        if self.db_driver.room_queries.has_available_room():
            self.new_reservation_dialog = NewReservationDialog()
            self.new_reservation_dialog_controller = NewReservationDialogController(self.new_reservation_dialog, self.db_driver)

            self.new_reservation_dialog.exec()

            self.refresh_reservations_data()
        else:
            self.no_room_dialog = FeedbackDialog(header_message="No more available rooms.",
                                                 subheader_message="Please try again later.")
            self.no_room_dialog.exec()

    def open_reservation_info_dialog(self, index):
        selected_reservation_id = index.sibling(index.row(), 0).data()

        selected_reservation_status = self.db_driver.reserved_room_queries.get_specific_reservation_details('reservation_status',
                                                                                                            selected_reservation_id)

        if selected_reservation_status == 'pending':
            view_type = 'current'
        else:
            view_type = 'past'

        self.reservation_info_dialog = ReservationInfoDialog(view_type)
        self.reservation_info_dialog_controller = ReservationInfoDialogController(self.reservation_info_dialog,
                                                                                  self.db_driver,
                                                                                  selected_reservation_id,
                                                                                  view_type=view_type)

        self.reservation_info_dialog.exec()

        self.refresh_reservations_data()

    def update_row_count(self):
        current_max_reservations_per_page = self.view.get_max_rows_of_reservations_table_view()

        if current_max_reservations_per_page != 0 and self.max_reservations_per_page != current_max_reservations_per_page:

            self.max_reservations_per_page = current_max_reservations_per_page

            self.view.reservations_table_view.setUpdatesEnabled(False)
            self.refresh_reservations_data()
            self.view.reservations_table_view.setUpdatesEnabled(True)
            self.view.reservations_table_view.viewport().update()

    def connect_signals_to_slots(self):
        self.view.window_resized.connect(self.update_row_count)

        self.view.sort_by_combobox.currentTextChanged.connect(self.refresh_reservations_data)
        self.view.sort_type_combobox.currentTextChanged.connect(self.refresh_reservations_data)
        self.view.view_type_combobox.currentTextChanged.connect(self.refresh_reservations_data)

        self.view.clicked_add_reservation_button.connect(self.open_new_reservation_dialog)

        self.view.clicked_info_button.connect(self.open_reservation_info_dialog)
        self.view.clicked_check_in_button.connect(self.convert_reservation_to_booking)

        self.view.search_text_changed.connect(self.update_prev_search_input)
        self.view.search_text_changed.connect(lambda _: self.refresh_reservations_data())

        self.view.next_page_button_pressed.connect(self.go_to_next_page)
        self.view.previous_page_button_pressed.connect(self.go_to_previous_page)

    def convert_reservation_to_booking(self, index):

        selected_payment_status = index.sibling(index.row(), 5).data()

        if selected_payment_status == "fully paid":
            selected_reservation_id = index.sibling(index.row(), 0).data()

            self.confirmation_dialog = ConfirmationDialog(f"Confirm check-in of {selected_reservation_id}?")

            self.confirmation_dialog.exec()

            if self.confirmation_dialog.get_choice():
                check_in_date, check_out_date = index.sibling(index.row(), 4).data().split("-")
                reservation_room_number = index.sibling(index.row(), 2).data()

                booking_inputs = {"check_in_status": "in progress",
                                  "check_in_date": datetime.strptime(check_in_date.strip(), "%b %d, %Y"),
                                  "check_out_date": datetime.strptime(check_out_date.strip(), "%b %d, %Y"),
                                  "actual_check_in_date": datetime.now(),
                                  "actual_check_out_date": None,
                                  "guest_id": self.db_driver.reserved_room_queries.get_specific_reservation_details('guest_id', selected_reservation_id),
                                  "room_number": reservation_room_number}

                self.db_driver.booked_room_queries.add_booked_room(booking_inputs)
                self.db_driver.reserved_room_queries.set_reservation_status('confirmed', selected_reservation_id)
                self.db_driver.room_queries.set_room_status(reservation_room_number, 'occupied')

                self.update_reservations_table_view()

                latest_booking_id = self.db_driver.booked_room_queries.get_latest_booking_id()

                self.feedback_dialog = FeedbackDialog("Reservation converted to booking!",
                                                      f"The booking id is {latest_booking_id}.")
                self.feedback_dialog.exec()

        else:
            self.feedback_dialog = FeedbackDialog("Remaining balance detected.", "Complete payment to proceed.")
            self.feedback_dialog.exec()

    def update_prev_search_input(self, search_input):
        self.prev_search_input = search_input

    def go_to_next_page(self):
        reservation_count = self.db_driver.reserved_room_queries.get_reservation_count(view_type=self.prev_view_type,
                                                                                       search_input=self.prev_search_input)

        if self.current_page_number + 1 <= self.total_pages(reservation_count):
            self.current_page_number += 1

            self.refresh_reservations_data()

    def go_to_previous_page(self):
        if self.current_page_number > 1:
            self.current_page_number -= 1
            self.refresh_reservations_data()

    def total_pages(self, reservations_count):
        return (reservations_count + self.max_reservations_per_page - 1) // self.max_reservations_per_page

    def refresh_reservations_data(self):
        self.prev_view_type = self.view.view_type_combobox.currentText()
        self.prev_sort_by = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        self.prev_sort_type = self.view.sort_type_combobox.currentText()

        self.set_models()

        self.check_if_underflow_contents()

    def check_if_underflow_contents(self):
        if self.reservations_model.get_len_of_data() == 0:
            self.go_to_previous_page()

    def set_models(self):
        reservations_data_from_db = self.db_driver.reserved_room_queries.get_all_reservations(enable_pagination=True,
                                                                                              max_reservations_per_page=self.max_reservations_per_page,
                                                                                              current_page_number=self.current_page_number,
                                                                                              view_type=self.prev_view_type,
                                                                                              sort_by=self.prev_sort_by,
                                                                                              sort_type=self.prev_sort_type,
                                                                                              search_input=self.prev_search_input)

        if not self.reservations_model:
            self.reservations_model = ReservationModel(reservations_data_from_db, "reservation_page_view")
            self.view.reservations_table_view.setModel(self.reservations_model)
            self.view.set_table_views_column_widths()
        else:
            self.reservations_model.update_data(reservations_data_from_db)
