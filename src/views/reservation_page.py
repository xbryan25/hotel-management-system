from PyQt6.QtWidgets import QWidget

from ui.reservation_page_ui import Ui_Widget as ReservationPageUI


class ReservationPage(QWidget, ReservationPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
