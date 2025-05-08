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

        self.set_external_stylesheet()
        self.load_fonts()

        self.is_current_date_today()

    def set_text_in_labels(self):
        self.day_number.setText(self.current_date.strftime("%b %d"))
        self.weekday_name.setText(self.current_date.strftime("%a"))

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
                           background-color: #194FCC;
                           border: 2px solid #000000;
                           border-radius: 5px;
                        }
                        #day_number, #weekday_name{
                           color: white;
                        }
                   """)

    def set_external_stylesheet(self):
        with open("../resources/styles/day_frame.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.day_number.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.weekday_name.setFont(QFont("Inter", 13, QFont.Weight.Normal))

    def mousePressEvent(self, event):
        self.clicked.emit(self.current_date)
        super().mousePressEvent(event)
