from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt

from datetime import datetime

from ui import AddEditServiceDialogUI
from views import ConfirmationDialog, FeedbackDialog


class AddEditServiceDialog(QDialog, AddEditServiceDialogUI):
    clicked_add_service_button = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()

    def validate_form_completion(self):

        # TODO: Also check if service name already exists or not
        if self.service_name_lineedit.text().strip() != '':
            self.confirm_service()
        else:
            self.warning_dialog = FeedbackDialog("Service name is blank.")
            self.warning_dialog.exec()

    def confirm_service(self):
        header_message = "Are you sure you want to add this service?"
        subheader_message = "Double check all input fields before proceeding."
        self.confirmation_dialog = ConfirmationDialog(header_message, subheader_message)

        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_choice():
            self.clicked_add_service_button.emit()

    def get_service_inputs(self):
        service_inputs = {}

        service_inputs.update({"service_name": self.service_name_lineedit.text()})
        service_inputs.update({"rate": self.rate_spinbox.value()})

        return service_inputs

    def connect_signals_to_slots(self):

        self.add_service_button.clicked.connect(self.validate_form_completion)
        self.cancel_button.clicked.connect(self.close)

    def set_external_stylesheet(self):
        with open("../resources/styles/add_edit_service_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.add_new_service_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.cancel_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.add_service_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.service_name_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.rate_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.service_name_lineedit.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.rate_spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
