from PyQt6.QtWidgets import QWidget

from ui import CalendarPageUI


class CalendarPage(QWidget, CalendarPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
