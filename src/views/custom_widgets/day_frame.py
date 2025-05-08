from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtCore import QSize, pyqtSignal

from datetime import date

from ui.day_frame_ui import Ui_Frame as DayFrameUI


class DayFrame(QFrame, DayFrameUI):
    clicked = pyqtSignal(date)

    def __init__(self, current_date):
        super().__init__()

        self.setupUi(self)
        self.current_date = current_date

        self.set_text_in_labels()

        self.setStyleSheet("QFrame#Frame{border: 1px solid black;}")
        self.is_current_date_today()

    def set_text_in_labels(self):
        self.day_number.setText(self.current_date.strftime("%a"))
        self.weekday_name.setText(self.current_date.strftime("%b %d"))

    def update_current_date(self, current_date):
        self.current_date = current_date
        self.set_text_in_labels()
        self.is_current_date_today()

    def get_current_date(self):
        return self.current_date

    def is_current_date_today(self):
        if self.current_date == date.today():
            self.setStyleSheet("""
                       QFrame#Frame {
                           background-color: blue;
                       }
                       #day_number, #weekday_name{
                           color: white;
                       }
                   """)
        else:
            self.setStyleSheet("QFrame#Frame{background-color: transparent;}")

    def mousePressEvent(self, event):
        self.clicked.emit(self.current_date)
        super().mousePressEvent(event)
