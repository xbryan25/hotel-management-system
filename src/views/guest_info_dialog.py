from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import pyqtSignal

from ui.guest_info_dialog_ui import Ui_Dialog as GuestInfoDialogUI


class GuestInfoDialog(QDialog, GuestInfoDialogUI):

    mode_changed = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.setupUi(self)

        self.connect_default_signals_to_slots()

        self.information_mode = "view"

    def set_guest_info(self, guest_info):
        if self.information_mode == "edit":
            self.guest_id_lineedit.setPlaceholderText(guest_info["guest_id"])
            self.name_lineedit.setPlaceholderText(guest_info["name"])
            self.sex_lineedit.setPlaceholderText(guest_info["sex"].capitalize())
            self.home_address_lineedit.setPlaceholderText(guest_info["home_address"])
            self.email_address_lineedit.setPlaceholderText(guest_info["email_address"])
            self.phone_number_lineedit.setPlaceholderText(guest_info["phone_number"])
            self.birth_date_lineedit.setPlaceholderText(guest_info["birth_date"].strftime("%b %d, %Y"))
            self.government_id_lineedit.setPlaceholderText(guest_info["government_id"])

        else:
            self.guest_id_value_label.setText(guest_info["guest_id"])
            self.name_value_label.setText(guest_info["name"])
            self.sex_value_label.setText(guest_info["sex"])
            self.home_address_value_label.setText(guest_info["home_address"])
            self.email_address_value_label.setText(guest_info["email_address"])
            self.phone_number_value_label.setText(guest_info["phone_number"])
            self.birth_date_value_label.setText(guest_info["birth_date"].strftime("%b %d, %Y"))
            self.government_id_value_label.setText(guest_info["government_id"])

        self.last_visit_date_value_label.setText(guest_info["last_visit_date"])
        self.total_visit_count_value_label.setText(str(guest_info["total_visit_count"]))
        self.total_amount_due_value_label.setText(guest_info["total_amount_due"])

    # def change_information_mode(self):
    #     if self.information_mode == "view":
    #         self.information_mode = "edit"
    #         self.information_stacked_widget.setCurrentWidget(self.edit_mode_widget)
    #     elif self.information_mode == "edit":
    #         self.information_mode = "view"
    #         self.information_stacked_widget.setCurrentWidget(self.view_mode_widget)

    def confirm_edit_status(self):
        self.disconnect_signals()
        self.left_button.setText("Proceed editing?")
        self.right_button.setText("Cancel editing?")

        self.left_button.clicked.connect(lambda: print("Edited guest"))
        self.right_button.clicked.connect(self.reconnect_to_default_signals)

        self.information_stacked_widget.setCurrentWidget(self.edit_mode_widget)
        self.information_mode = "edit"
        self.mode_changed.emit()

    def confirm_delete_status(self):
        self.disconnect_signals()
        self.left_button.setText("Proceed deletion?")
        self.right_button.setText("Cancel deletion?")

        self.left_button.clicked.connect(lambda: print("Deleted guest"))
        self.right_button.clicked.connect(self.reconnect_to_default_signals)

    def load_fonts(self):
        pass

    def set_external_stylesheet(self):
        pass

    def connect_default_signals_to_slots(self):
        # Add signal to call controller that mode is changed, to call set_guest_info_again
        self.left_button.clicked.connect(self.confirm_edit_status)
        self.right_button.clicked.connect(self.confirm_delete_status)

    def disconnect_signals(self):
        try:
            self.left_button.clicked.disconnect()
            self.right_button.clicked.disconnect()
        except TypeError:
            pass

    def reconnect_to_default_signals(self):
        self.disconnect_signals()
        self.connect_default_signals_to_slots()

        self.left_button.setText("Edit Guest")
        self.right_button.setText("Delete Guest")

        self.information_stacked_widget.setCurrentWidget(self.view_mode_widget)
        self.information_mode = "view"

