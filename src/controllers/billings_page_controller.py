from datetime import datetime

from models import ReservationModel
from views import ConfirmationDialog, FeedbackDialog, AddPaymentDialog
from controllers.add_payment_dialog_controller import AddPaymentDialogController


class BillingsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.set_models()

        self.view.set_table_views_column_widths()

    def connect_signals_to_slots(self):
        self.view.sort_by_combobox.currentTextChanged.connect(self.update_billings_table_view)
        self.view.sort_type_combobox.currentTextChanged.connect(self.update_billings_table_view)
        self.view.view_type_combobox.currentTextChanged.connect(self.update_billings_table_view)

        # self.view.clicked_info_button.connect(lambda: print("clicked info button"))
        self.view.clicked_add_payment_button.connect(self.open_add_payment_dialog)

    def open_add_payment_dialog(self, index):
        data_from_row = {"reservation_id": index.sibling(index.row(), 0).data(),
                         "remaining_balance": index.sibling(index.row(), 4).data()}

        self.add_payment_dialog = AddPaymentDialog()
        self.add_payment_dialog_controller = AddPaymentDialogController(self.add_payment_dialog, self.db_driver, data_from_row)

        self.add_payment_dialog.exec()

        self.update_billings_table_view()

    def set_models(self):
        reservations_initial_data = self.db_driver.reserved_room_queries.get_all_reservations(view_type="Billings",
                                                                                              billing_view_mode=True)

        self.reservation_table_model = ReservationModel(reservations_initial_data, "billing_page_view")

        self.view.billings_table_view.setModel(self.reservation_table_model)

    def update_billings_table_view(self):
        sort_by_text = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        sort_type_text = self.view.sort_type_combobox.currentText()
        view_type_text = self.view.view_type_combobox.currentText()

        reservations_data_from_db = self.db_driver.reserved_room_queries.get_all_reservations(sort_by=sort_by_text,
                                                                                              sort_type=sort_type_text,
                                                                                              view_type=view_type_text,
                                                                                              billing_view_mode=True)

        self.reservation_table_model.update_data(reservations_data_from_db)
