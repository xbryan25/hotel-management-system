from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtGui import QFont

from datetime import date

from ui import GuestInfoDialogUI


class GuestInfoDialog(QDialog, GuestInfoDialogUI):

    mode_changed = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.setupUi(self)

        self.connect_default_signals_to_slots()

        self.set_external_stylesheet()
        self.load_fonts()

        self.information_mode = "view"

    @staticmethod
    def truncate_text(text, max_length=20):
        if len(text) <= max_length:
            return filename
        return text[:max_length] + "..."

    def set_guest_info(self, guest_info):
        if self.information_mode == "edit":
            birth_date = guest_info["birth_date"]
            q_date = QDate(birth_date.year, birth_date.month, birth_date.day)

            self.name_lineedit.setPlaceholderText(guest_info["name"])
            self.gender_combobox.setCurrentText(guest_info["gender"])
            self.home_address_lineedit.setPlaceholderText(guest_info["home_address"])
            self.email_address_lineedit.setPlaceholderText(guest_info["email_address"])
            self.phone_number_lineedit.setPlaceholderText(guest_info["phone_number"])
            self.birth_date_date_edit.setDate(q_date)
            self.government_id_number_lineedit.setPlaceholderText(guest_info["government_id"])

        else:
            self.guest_id_value_label.setText(guest_info["guest_id"])
            self.name_value_label.setText(guest_info["name"])
            self.gender_value_label.setText(guest_info["gender"])
            self.home_address_value_label.setText(guest_info["home_address"])
            self.email_address_value_label.setText(guest_info["email_address"])
            self.phone_number_value_label.setText(guest_info["phone_number"])
            self.birth_date_value_label.setText(guest_info["birth_date"].strftime("%b %d, %Y"))
            self.government_id_number_value_label.setText(guest_info["government_id"])

            self.name_value_label.setText(self.truncate_text(guest_info["name"]))
            self.name_value_label.setToolTip(guest_info["name"])

            self.home_address_value_label.setText(self.truncate_text(guest_info["home_address"]))
            self.home_address_value_label.setToolTip(guest_info["home_address"])

            self.email_address_value_label.setText(self.truncate_text(guest_info["email_address"]))
            self.email_address_value_label.setToolTip(guest_info["email_address"])

            self.government_id_number_value_label.setText(self.truncate_text(guest_info["government_id"]))
            self.government_id_number_value_label.setToolTip(guest_info["government_id"])

        if isinstance(guest_info["last_visit_date"], date):
            self.last_visit_date_value_label.setText(guest_info["last_visit_date"].strftime("%b %d, %Y"))
        else:
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
        self.guest_details_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.guest_id_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.name_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.gender_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.home_address_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.email_address_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.phone_number_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.birth_date_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.government_id_number_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.last_visit_date_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.total_visit_count_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.total_amount_due_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        
        self.guest_id_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.name_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.gender_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.home_address_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.email_address_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.phone_number_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.birth_date_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.government_id_number_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.last_visit_date_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.total_visit_count_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.total_amount_due_value_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))

        self.name_lineedit.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.gender_combobox.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.home_address_lineedit.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.email_address_lineedit.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.phone_number_lineedit.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.birth_date_date_edit.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.government_id_number_lineedit.setFont(QFont("Inter", 11, QFont.Weight.Normal))

        self.left_button.setFont(QFont("Inter", 10, QFont.Weight.Bold))
        self.right_button.setFont(QFont("Inter", 10, QFont.Weight.Bold))

    def set_external_stylesheet(self):
        with open("../resources/styles/guest_info_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

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

