from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt

from datetime import datetime

from ui import AddRoomDialogUI
from views import ConfirmationDialog, FeedbackDialog


class AddRoomDialog(QDialog, AddRoomDialogUI):
    # clicked_add_payment_button = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.connect_signals_to_slots()
        #
        self.load_fonts()
        self.set_external_stylesheet()

    def set_external_stylesheet(self):
        with open("../resources/styles/add_room_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.add_new_room_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.room_details_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))

        self.cancel_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.add_room_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.room_type_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_type_value_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_daily_rate_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_daily_rate_spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_capacity_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_capacity_spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_image_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.chosen_image_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.browse_image_button.setFont(QFont("Inter", 12, QFont.Weight.Bold))
