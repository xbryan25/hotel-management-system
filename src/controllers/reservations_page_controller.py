from models import ReservationModel
from views import NewReservationDialog
from views.message_dialogs import ConfirmationDialog, FeedbackDialog
from controllers.new_reservation_dialog_controller import NewReservationDialogController


class ReservationsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.set_models()

        self.view.set_table_views_column_widths()

    def open_new_reservation_dialog(self):
        self.new_reservation_dialog = NewReservationDialog()
        self.new_reservation_dialog_controller = NewReservationDialogController(self.new_reservation_dialog, self.db_driver)

        self.new_reservation_dialog.exec()

        self.update_reservations_table_view()

    def connect_signals_to_slots(self):
        self.view.sort_by_combobox.currentTextChanged.connect(self.update_reservations_table_view)
        self.view.sort_type_combobox.currentTextChanged.connect(self.update_reservations_table_view)
        self.view.view_type_combobox.currentTextChanged.connect(self.update_reservations_table_view)

        self.view.clicked_add_reservation_button.connect(self.open_new_reservation_dialog)

        self.view.clicked_info_button.connect(lambda: print("clicked info button"))
        self.view.clicked_check_in_button.connect(self.convert_reservation_to_booking)

    def convert_reservation_to_booking(self, index):

        selected_payment_status = index.sibling(index.row(), 5).data()

        if selected_payment_status == "fully paid":
            selected_reservation_id = index.sibling(index.row(), 0).data()

            self.confirmation_dialog = ConfirmationDialog(f"Confirm check-in of {selected_reservation_id}?")

            self.confirmation_dialog.exec()

            print(self.confirmation_dialog.get_choice())

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
