from datetime import datetime

from models import ReservationModel
from views import ConfirmationDialog, FeedbackDialog, AddPaymentDialog
from controllers.add_payment_dialog_controller import AddPaymentDialogController


class BillingsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.billings_model = None

        self.prev_view_type = None
        self.prev_sort_by = None
        self.prev_sort_type = None
        self.prev_search_input = None

        self.current_page_number = 1
        self.max_billings_per_page = 16

    def update_row_count(self):
        current_max_billings_per_page = self.view.get_max_rows_of_billings_table_view()

        if current_max_billings_per_page != 0 and self.max_billings_per_page != current_max_billings_per_page:

            self.max_billings_per_page = current_max_billings_per_page

            self.view.billings_table_view.setUpdatesEnabled(False)
            self.refresh_billings_data()
            self.view.billings_table_view.setUpdatesEnabled(True)
            self.view.billings_table_view.viewport().update()

    def connect_signals_to_slots(self):
        self.view.window_resized.connect(self.update_row_count)

        self.view.sort_by_combobox.currentTextChanged.connect(self.refresh_billings_data)
        self.view.sort_type_combobox.currentTextChanged.connect(self.refresh_billings_data)
        self.view.view_type_combobox.currentTextChanged.connect(self.refresh_billings_data)

        self.view.clicked_add_payment_button.connect(self.open_add_payment_dialog)

        self.view.search_text_changed.connect(self.update_prev_search_input)
        self.view.search_text_changed.connect(lambda _: self.refresh_billings_data())

        self.view.next_page_button_pressed.connect(self.go_to_next_page)
        self.view.previous_page_button_pressed.connect(self.go_to_previous_page)

    def open_add_payment_dialog(self, index):
        data_from_row = {"reservation_id": index.sibling(index.row(), 0).data(),
                         "remaining_balance": index.sibling(index.row(), 4).data()}

        self.add_payment_dialog = AddPaymentDialog()
        self.add_payment_dialog_controller = AddPaymentDialogController(self.add_payment_dialog, self.db_driver, data_from_row)

        self.add_payment_dialog.exec()

        self.refresh_billings_data()

    def update_prev_search_input(self, search_input):
        self.prev_search_input = search_input

    def go_to_next_page(self):
        billings_count = self.db_driver.reserved_room_queries.get_reservation_count(view_type=self.prev_view_type,
                                                                                    search_input=self.prev_search_input,
                                                                                    billing_view_mode=True)

        if self.current_page_number + 1 <= self.total_pages(billings_count):
            self.current_page_number += 1

            self.refresh_billings_data()

    def go_to_previous_page(self):
        if self.current_page_number > 1:
            self.current_page_number -= 1
            self.refresh_billings_data()

    def total_pages(self, billings_count):
        return (billings_count + self.max_billings_per_page - 1) // self.max_billings_per_page

    def refresh_billings_data(self):
        self.prev_view_type = self.view.view_type_combobox.currentText()
        self.prev_sort_by = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        self.prev_sort_type = self.view.sort_type_combobox.currentText()

        self.set_models()

        self.check_if_underflow_contents()

    def check_if_underflow_contents(self):
        if self.billings_model.get_len_of_data() == 0:
            self.go_to_previous_page()

    def set_models(self):
        billings_data_from_db = self.db_driver.reserved_room_queries.get_all_reservations(enable_pagination=True,
                                                                                          max_reservations_per_page=self.max_billings_per_page,
                                                                                          current_page_number=self.current_page_number,
                                                                                          view_type=self.prev_view_type,
                                                                                          sort_by=self.prev_sort_by,
                                                                                          sort_type=self.prev_sort_type,
                                                                                          search_input=self.prev_search_input,
                                                                                          billing_view_mode=True)

        if not self.billings_model:
            self.billings_model = ReservationModel(billings_data_from_db, "billing_page_view")
            self.view.billings_table_view.setModel(self.billings_model)
            self.view.set_table_views_column_widths()
        else:
            self.billings_model.update_data(billings_data_from_db)
