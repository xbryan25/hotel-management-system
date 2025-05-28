from models import ServicesModel
from views import AddEditServiceDialog, ConfirmationDialog, FeedbackDialog

from controllers.add_edit_service_dialog_controller import AddEditServiceDialogController


class ServicesPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget

        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.services_model = None

        self.prev_view_type = None
        self.prev_sort_by = None
        self.prev_sort_type = None
        self.prev_search_input = None

        self.current_page = 1
        self.max_services_per_page = 16

    def set_page_number_lineedit_validator(self, total_pages):
        self.view.set_page_number_lineedit_validator(total_pages)

    def open_add_edit_service_dialog(self, dialog_type, index=None):

        if index:
            selected_service_id = index.sibling(index.row(), 0).data()
        else:
            selected_service_id = None

        self.add_edit_service_dialog = AddEditServiceDialog()
        self.add_edit_service_controller = AddEditServiceDialogController(self.add_edit_service_dialog, self.db_driver,
                                                                          dialog_type, selected_service_id)

        self.add_edit_service_dialog.exec()

        self.refresh_services_data()

    def set_service_active_status(self, index):

        selected_service_id = index.sibling(index.row(), 0).data()

        if self.db_driver.service_queries.get_service_active_status(selected_service_id):
            delete_or_restore = "Delete"
            is_active = False
        else:
            delete_or_restore = "Restore"
            is_active = True

        self.confirmation_dialog = ConfirmationDialog(f"{delete_or_restore} {selected_service_id}?")
        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_choice():
            self.db_driver.service_queries.set_service_active_status(is_active, selected_service_id)

            self.refresh_services_data()

            self.feedback_dialog = FeedbackDialog(f"{delete_or_restore}d {selected_service_id}.")
            self.feedback_dialog.exec()

    def update_row_count(self):
        current_max_services_per_page = self.view.get_max_rows_of_services_table_view()

        if current_max_services_per_page != 0 and self.max_services_per_page != current_max_services_per_page:

            self.max_services_per_page = current_max_services_per_page

            self.view.services_table_view.setUpdatesEnabled(False)
            self.refresh_services_data()
            self.view.services_table_view.setUpdatesEnabled(True)
            self.view.services_table_view.viewport().update()

    def connect_signals_to_slots(self):
        self.view.window_resized.connect(self.update_row_count)

        self.view.sort_by_combobox.currentTextChanged.connect(self.refresh_services_data)
        self.view.sort_type_combobox.currentTextChanged.connect(self.refresh_services_data)
        self.view.view_type_combobox.currentTextChanged.connect(self.refresh_services_data)

        self.view.clicked_add_service_button.connect(lambda: self.open_add_edit_service_dialog("add_service"))

        self.view.clicked_edit_button.connect(self.open_add_edit_service_dialog)
        self.view.clicked_change_active_status_button.connect(self.set_service_active_status)

        self.view.search_text_changed.connect(self.update_prev_search_input)
        self.view.search_text_changed.connect(lambda _: self.refresh_services_data())

        self.view.next_page_button_pressed.connect(self.go_to_next_page)
        self.view.previous_page_button_pressed.connect(self.go_to_previous_page)

        self.view.page_number_lineedit_changed.connect(self.change_page_number_lineedit)

    def change_page_number_lineedit(self, page_number):

        service_count = self.db_driver.service_queries.get_service_count(view_type=self.prev_view_type,
                                                                         search_input=self.prev_search_input)
        total_pages = max(self.total_pages(service_count), 1)

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

        self.refresh_services_data()

    def update_prev_search_input(self, search_input):
        self.prev_search_input = search_input

    def go_to_next_page(self):
        service_count = self.db_driver.service_queries.get_service_count(view_type=self.prev_view_type,
                                                                         search_input=self.prev_search_input)

        if self.current_page + 1 <= self.total_pages(service_count):
            self.current_page += 1

            self.view.page_number_lineedit.blockSignals(True)
            self.view.page_number_lineedit.setText(str(self.current_page))
            self.view.page_number_lineedit.blockSignals(False)

            self.refresh_services_data()

    def go_to_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1

            self.view.page_number_lineedit.blockSignals(True)
            self.view.page_number_lineedit.setText(str(self.current_page))
            self.view.page_number_lineedit.blockSignals(False)

            self.refresh_services_data()

    def total_pages(self, services_count):
        return (services_count + self.max_services_per_page - 1) // self.max_services_per_page

    def refresh_services_data(self):
        self.prev_view_type = self.view.view_type_combobox.currentText()
        self.prev_sort_by = self.view.sort_by_combobox.currentText().replace("Sort by ", "")
        self.prev_sort_type = self.view.sort_type_combobox.currentText()

        self.set_models()

        self.check_if_underflow_contents()

    def check_if_underflow_contents(self):
        if self.services_model.get_len_of_data() == 0:
            self.go_to_previous_page()

    def set_models(self):
        services_data_from_db = self.db_driver.service_queries.get_all_services(enable_pagination=True,
                                                                                max_services_per_page=self.max_services_per_page,
                                                                                current_page=self.current_page,
                                                                                view_type=self.prev_view_type,
                                                                                sort_by=self.prev_sort_by,
                                                                                sort_type=self.prev_sort_type,
                                                                                search_input=self.prev_search_input)

        if not self.services_model:
            self.services_model = ServicesModel(services_data_from_db)
            self.view.services_table_view.setModel(self.services_model)
            self.view.services_table_view.hide_first_column()
            self.view.set_table_views_column_widths()
        else:
            self.services_model.update_data(services_data_from_db)

        service_count = self.db_driver.service_queries.get_service_count(view_type=self.prev_view_type,
                                                                         search_input=self.prev_search_input)

        self.set_page_number_lineedit_validator(self.total_pages(service_count))
        self.view.update_of_page_number_label(self.total_pages(service_count))
