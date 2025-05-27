from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont

from ui import ConfirmationDialogUI


class ConfirmationDialog(QDialog, ConfirmationDialogUI):
    def __init__(self, header_message, subheader_message=None, left_button_text=None, right_button_text=None):
        super().__init__()

        self.setupUi(self)

        self.set_messages(header_message, subheader_message, left_button_text, right_button_text)
        self.connect_signals_to_slots()

        self.choice = False

        self.load_fonts()
        self.set_external_stylesheet()

        self.setWindowTitle("HotelEase")

    def set_messages(self, header_message, subheader_message, left_button_text, right_button_text):
        self.header_message_label.setText(header_message)

        if not subheader_message:
            self.subheader_message_label.setVisible(False)
        else:
            self.subheader_message_label.setText(subheader_message)

        if not left_button_text:
            self.left_button.setText("No")
        else:
            self.left_button.setText(left_button_text)

        if not right_button_text:
            self.right_button.setText("Yes")
        else:
            self.right_button.setText(right_button_text)

    def connect_signals_to_slots(self):
        self.left_button.clicked.connect(self.set_choice_to_no)
        self.right_button.clicked.connect(self.set_choice_to_yes)

    def set_choice_to_no(self):
        self.choice = False
        self.close()

    def set_choice_to_yes(self):
        self.choice = True
        self.close()

    def get_choice(self):
        return self.choice

    def set_external_stylesheet(self):
        with open("../resources/styles/confirmation_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.header_message_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.subheader_message_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))

        self.left_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.right_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))


