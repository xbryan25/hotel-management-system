from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox
from PyQt6.QtGui import QCursor, QFont, QIntValidator
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt

from datetime import datetime
import os

from ui import AddEditRoomDialogUI
from views import ConfirmationDialog, FeedbackDialog


class AddEditRoomDialog(QDialog, AddEditRoomDialogUI):
    clicked_add_edit_room_button = pyqtSignal(str)
    clicked_browse_image_button = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()

        self.set_room_number_lineedit_validator()

    def load_edit_room_view(self, room_number, room_details):
        self.room_label.setText(f"Edit {room_number}")
        self.right_button.setText("Edit room")

        self.room_daily_rate_spinbox.setValue(room_details[2])
        self.room_capacity_spinbox.setValue(room_details[4])
        self.room_type_value_combobox.setCurrentText(room_details[1])
        self.room_number_lineedit.setText(room_number.replace("room-", ""))

    def update_chosen_image_label(self, filename):
        self.chosen_image_label.setText(self.truncate_filename_preserving_ext(filename))
        self.chosen_image_label.setToolTip(filename)

    @staticmethod
    def truncate_filename_preserving_ext(filename, max_length=20):
        name, ext = os.path.splitext(filename)
        if len(filename) <= max_length:
            return filename
        return name[:max_length - len(ext) - 3] + "..." + ext

    def set_room_number_lineedit_validator(self):

        validator = QIntValidator(1000, 9999)
        self.room_number_lineedit.setValidator(validator)
        self.room_number_lineedit.setMaxLength(4)

    def confirm_room_addition(self, room_number):
        header_message = "Are you sure you to add this room?"
        subheader_message = "Double check all input fields before proceeding."
        self.confirmation_dialog = ConfirmationDialog(header_message, subheader_message)

        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_choice():
            self.clicked_add_edit_room_button.emit("room-" + room_number)

    def validate_form_completion(self):
        has_chosen_image = True
        has_room_type = True
        is_proper_room_number = True

        room_type = self.room_type_value_combobox.currentText()
        chosen_image = self.chosen_image_label.text()
        room_number = self.room_number_lineedit.text()

        if not chosen_image:
            has_chosen_image = False

        if not room_type:
            has_room_type = False

        if len(room_number) != 4 and self.room_number_lineedit.isVisible():
            is_proper_room_number = False

        if has_chosen_image and has_room_type and is_proper_room_number:
            self.confirm_room_addition(room_number)
        else:
            false_count = sum(not x for x in [has_chosen_image, has_room_type, is_proper_room_number])

            header_message = None
            subheader_message = None

            if false_count >= 2:
                header_message = "At least one of the fields has a wrong input."
                subheader_message = "Please recheck."

            elif not is_proper_room_number:
                header_message = "Room number is not in the proper format."
                subheader_message = "Format: room-XXXX"

            elif not has_chosen_image:
                header_message = "Image has not been chosen."
                subheader_message = "Please choose an image."

            elif not has_room_type:
                header_message = "Room type is blank."
                subheader_message = "Please select or input a room type."

            self.warning_dialog = FeedbackDialog(header_message, subheader_message)
            self.warning_dialog.exec()

    def get_room_detail_inputs(self):
        room_detail_inputs = {}

        room_detail_inputs.update({"room_number": "room-" + self.room_number_lineedit.text()})
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

        self.room_number_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_leading_text_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.room_number_lineedit.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_image_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.chosen_image_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.browse_image_button.setFont(QFont("Inter", 12, QFont.Weight.Bold))
