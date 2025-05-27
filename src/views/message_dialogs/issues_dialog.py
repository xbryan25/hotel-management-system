from PyQt6.QtWidgets import QDialog, QWidget
from PyQt6.QtGui import QFont

from ui import IssuesDialogUI


class IssuesDialog(QDialog, IssuesDialogUI):
    def __init__(self, header_message, issues_message, connected_view=None, proceed_button_text=None):
        super().__init__()

        self.setupUi(self)

        self.connected_view = connected_view

        self.set_messages(header_message, issues_message, proceed_button_text)
        self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()

        self.setWindowTitle("HotelEase")

    def set_messages(self, header_message, issues_message, proceed_button_text):
        self.header_message_label.setText(header_message)

        self.issues_label.setText(issues_message)

        if not proceed_button_text:
            self.proceed_button.setText("Proceed")
        else:
            self.proceed_button.setText(left_button_text)

    def connect_signals_to_slots(self):
        self.proceed_button.clicked.connect(self.close_dialog)

    def close_dialog(self):
        if self.connected_view and isinstance(self.connected_view, QWidget):
            self.connected_view.close()

        self.close()

    def set_external_stylesheet(self):
        with open("../resources/styles/issues_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.header_message_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.issues_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.proceed_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))
