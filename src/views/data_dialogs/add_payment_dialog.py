from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt

from datetime import datetime

from ui import AddPaymentDialogUI
from views import ConfirmationDialog, FeedbackDialog


class AddPaymentDialog(QDialog, AddPaymentDialogUI):
    clicked_add_payment_button = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()

        self.setWindowTitle("HotelEase | Add Payment")

    def set_remaining_balance_value(self, remaining_balance):
        self.remaining_balance_value_label.setText(f"₱{remaining_balance}")

    def set_spinbox_max_value(self, remaining_balance):
        self.amount_spinbox.setMaximum(remaining_balance)

    def confirm_payment(self):
        header_message = "Are you sure you want to make this payment?"
        subheader_message = "Double check all input fields before proceeding."
        self.confirmation_dialog = ConfirmationDialog(header_message, subheader_message)

        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_choice():
            self.clicked_add_payment_button.emit()

    def get_payment_inputs(self):
        payment_inputs = {}

        payment_inputs.update({"payment_type": self.payment_type_combobox.currentText()})
        payment_inputs.update({"amount": self.amount_spinbox.value()})
        payment_inputs.update({"transaction_date": datetime.now()})

        return payment_inputs

    def connect_signals_to_slots(self):

        self.add_payment_button.clicked.connect(self.confirm_payment)
        self.cancel_button.clicked.connect(self.close)

    def set_external_stylesheet(self):
        with open("../resources/styles/add_payment_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.add_new_payment_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.cancel_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.add_payment_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.remaining_balance_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.remaining_balance_value_label.setFont(QFont("Inter", 15, QFont.Weight.Normal))

        self.payment_type_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.amount_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.payment_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.amount_spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
