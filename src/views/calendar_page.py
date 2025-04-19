from PyQt6.QtWidgets import QWidget

from ui.calendar_page_ui import Ui_Widget as CalendarPageUI


class CalendarPage(QWidget, CalendarPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
