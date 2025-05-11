from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt

from datetime import datetime

from ui import AddPaymentDialogUI
from views import ConfirmationDialog, FeedbackDialog


class AddPaymentDialog(QDialog, AddPaymentDialogUI):
    clicked_add_payment_button = pyqtSignal()

    def __init__(self, remaining_balance):
        super().__init__()
        self.setupUi(self)

        self.remaining_balance = remaining_balance

        self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()

        self.set_text()
        self.set_spinbox_max_value()

    def set_text(self):
        self.remaining_balance_value_label.setText(f"₱{self.remaining_balance}")

    def set_spinbox_max_value(self):
        self.amount_spinbox.setMaximum(self.remaining_balance)

    def connect_signals_to_slots(self):

        self.add_payment_button.clicked.connect(self.clicked_add_payment_button.emit)

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
