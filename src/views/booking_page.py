from PyQt6.QtWidgets import QWidget

from ui.booking_page_ui import Ui_Widget as BookingPageUI


class BookingPage(QWidget, BookingPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
