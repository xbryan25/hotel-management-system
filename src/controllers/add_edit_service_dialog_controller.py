from PyQt6.QtWidgets import QSizePolicy, QSpacerItem

from views import FeedbackDialog


class AddEditServiceDialogController:
    def __init__(self, dialog, db_driver, dialog_type, service_id):
        self.view = dialog
        self.db_driver = db_driver

        self.dialog_type = dialog_type
        self.service_id = service_id

        self.connect_signals_to_slots()
        self.load_details_from_dialog_type()

    def load_details_from_dialog_type(self):
        if self.dialog_type == "edit_service":
            service_details = self.db_driver.service_queries.get_service_details(self.service_id)

            self.view.load_edit_service_view(self.service_id, service_details)

    def connect_signals_to_slots(self):
        self.view.clicked_right_button.connect(self.add_or_edit_service)

    def add_or_edit_service(self):
        service_inputs = self.view.get_service_inputs()

        service_name_existence = self.db_driver.service_queries.does_service_name_exist(service_inputs['service_name'])

        if not service_name_existence and self.dialog_type == "add_service":
            self.db_driver.service_queries.add_service(service_inputs)

            self.success_dialog = FeedbackDialog("Service added successfully.", connected_view=self.view)
            self.success_dialog.exec()
        elif (((not service_name_existence) or (service_name_existence and self.view.service_name_lineedit.text().strip() == ''))
              and self.dialog_type == "edit_service"):

            self.db_driver.service_queries.update_service(self.service_id, service_inputs)

            self.success_dialog = FeedbackDialog("Service updated successfully.", connected_view=self.view)
            self.success_dialog.exec()

        elif service_name_existence:
            self.fail_dialog = FeedbackDialog("Service name already exists.", "Please input another service name.")
            self.fail_dialog.exec()
