from PyQt6.QtWidgets import QSizePolicy, QSpacerItem

from models import GuestInfoModel
from views import FeedbackDialog


class GuestInfoDialogController:
    def __init__(self, dialog, db_driver, current_guest_id):
        self.view = dialog
        self.db_driver = db_driver
        self.current_guest_id = current_guest_id

        self.connect_signals_to_slots()

        self.load_data()

    def connect_signals_to_slots(self):
        self.view.mode_changed.connect(self.switch_information_mode_guest_info)

        self.view.clicked_edit_button.connect(self.update_guest_info)

    def load_data(self):
        guest_data = self.db_driver.guest_queries.get_guest_details(self.current_guest_id)
        self.current_guest_model = GuestInfoModel.from_list(guest_data)

        self.view.set_guest_info(self.current_guest_model.to_dict())

    def switch_information_mode_guest_info(self):
        self.view.set_guest_info(self.current_guest_model.to_dict())

    def update_guest_info(self):

        guest_inputs = self.view.get_guest_inputs()

        self.db_driver.guest_queries.update_guest(self.current_guest_id, guest_inputs)

        self.success_dialog = FeedbackDialog(f"{self.current_guest_id} edited successfully.", connected_view=self.view)
        self.success_dialog.exec()
