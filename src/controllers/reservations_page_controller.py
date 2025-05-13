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

        self.set_models()

        self.view.set_table_views_column_widths()

    def open_new_reservation_dialog(self):

        if self.db_driver.room_queries.has_available_room():
            self.new_reservation_dialog = NewReservationDialog()
            self.new_reservation_dialog_controller = NewReservationDialogController(self.new_reservation_dialog, self.db_driver)

            self.new_reservation_dialog.exec()

            self.update_reservations_table_view()
        else:
            self.no_room_dialog = FeedbackDialog(header_message="No more available rooms.",
                                                 subheader_message="Please try again later.")
            self.no_room_dialog.exec()

    def open_reservation_info_dialog(self, index):
        selected_reservation_id = index.sibling(index.row(), 0).data()

        self.reservation_info_dialog = ReservationInfoDialog()
        self.reservation_info_dialog_controller = ReservationInfoDialogController(self.reservation_info_dialog,
                                                                                  self.db_driver,
                                                                                  selected_reservation_id)

        self.reservation_info_dialog.exec()

        self.update_reservations_table_view()

    def connect_signals_to_slots(self):
        self.view.sort_by_combobox.currentTextChanged.connect(self.update_reservations_table_view)
        self.view.sort_type_combobox.currentTextChanged.connect(self.update_reservations_table_view)
        self.view.view_type_combobox.currentTextChanged.connect(self.update_reservations_table_view)

        self.view.clicked_add_reservation_button.connect(self.open_new_reservation_dialog)

        self.view.clicked_info_button.connect(self.open_reservation_info_dialog)
        self.view.clicked_check_in_button.connect(self.convert_reservation_to_booking)

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
