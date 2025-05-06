from PyQt6.QtWidgets import QWidget

from ui import ReservationPageUI


class ReservationPage(QWidget, ReservationPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
