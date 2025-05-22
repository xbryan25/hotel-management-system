from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont

from datetime import date

from ui import UpcomingReservationsDialogUI


class UpcomingReservationsDialog(QDialog, UpcomingReservationsDialogUI):
    mode_changed = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

    def setup_reservations_label(self, room_number):
        self.reservations_label.setText(f"Reservations of {room_number}")

    def load_fonts(self):
        self.reservations_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))

    def set_external_stylesheet(self):
        with open("../resources/styles/guest_info_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

