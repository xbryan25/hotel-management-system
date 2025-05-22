from PyQt6.QtWidgets import QSizePolicy, QSpacerItem

from views import FeedbackDialog


class AddEditServiceDialogController:
    def __init__(self, dialog, db_driver):
        self.view = dialog
        self.db_driver = db_driver

        self.connect_signals_to_slots()

    def connect_signals_to_slots(self):
        self.view.clicked_add_service_button.connect(self.add_service)

    def add_service(self):
        service_inputs = self.view.get_service_inputs()

        if self.db_driver.service_queries.does_service_name_exist(service_inputs['service_name']):
            self.fail_dialog = FeedbackDialog("Service name already exists.", "Please input another service name.")
            self.fail_dialog.exec()

        else:
            self.db_driver.service_queries.add_service(service_inputs)

            self.success_dialog = FeedbackDialog("Service added successfully.", connected_view=self.view)
            self.success_dialog.exec()
