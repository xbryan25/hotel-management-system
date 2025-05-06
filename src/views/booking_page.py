from PyQt6.QtWidgets import QWidget

from ui import BookingPageUI


class BookingPage(QWidget, BookingPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
