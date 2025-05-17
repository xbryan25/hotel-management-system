from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt

from datetime import datetime

from ui import AddEditRoomDialogUI
from views import ConfirmationDialog, FeedbackDialog


class AddEditRoomDialog(QDialog, AddEditRoomDialogUI):
    clicked_add_room_button = pyqtSignal()
    clicked_browse_image_button = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()

    def load_edit_room_view(self, room_number):
        self.room_label.setText(f"Edit {room_number}")
        self.right_button.setText("Edit room")

    def update_chosen_image_label(self, filename):
        self.chosen_image_label.setText(filename)

    def confirm_room_addition(self):
        header_message = "Are you sure you to add this room?"
        subheader_message = "Double check all input fields before proceeding."
        self.confirmation_dialog = ConfirmationDialog(header_message, subheader_message)

        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_choice():
            self.clicked_add_room_button.emit()

    def validate_form_completion(self):
        is_valid = True

        room_type = self.room_type_value_combobox.currentText()
        chosen_image = self.chosen_image_label.text()

        if not room_type or not chosen_image:
            is_valid = False

        if is_valid:
            self.confirm_room_addition()
        else:
            self.warning_dialog = FeedbackDialog("At least one of the fields is blank. Please recheck.")
            self.warning_dialog.exec()

    def get_room_detail_inputs(self):
        room_detail_inputs = {}

        room_detail_inputs.update({"room_type": self.room_type_value_combobox.currentText()})
        room_detail_inputs.update({"daily_rate": self.room_daily_rate_spinbox.value()})
        room_detail_inputs.update({"capacity": self.room_capacity_spinbox.value()})

        return room_detail_inputs

    def connect_signals_to_slots(self):
        self.left_button.clicked.connect(self.close)
        self.right_button.clicked.connect(self.validate_form_completion)
        self.browse_image_button.clicked.connect(self.clicked_browse_image_button.emit)

    def set_external_stylesheet(self):
        with open("../resources/styles/add_edit_room_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.room_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.room_details_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))

        self.left_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.right_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.room_type_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_type_value_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_daily_rate_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_daily_rate_spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_capacity_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_capacity_spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_image_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.chosen_image_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.browse_image_button.setFont(QFont("Inter", 12, QFont.Weight.Bold))
