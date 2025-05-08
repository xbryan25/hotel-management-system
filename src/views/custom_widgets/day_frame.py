from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtCore import QSize, pyqtSignal

from ui.day_frame_ui import Ui_Frame as DayFrameUI


class DayFrame(QFrame, DayFrameUI):
    clicked = pyqtSignal()

    def __init__(self, current_date):
        super().__init__()

        self.setupUi(self)
        self.current_date = current_date

        self.set_text_in_labels()

        self.setStyleSheet("QFrame#Frame{border: 1px solid black;}")

    def set_text_in_labels(self):
        self.day_number.setText(self.current_date.strftime("%a"))
        self.weekday_name.setText(self.current_date.strftime("%b %d"))

    def update_current_date(self, current_date):
        self.current_date = current_date
        self.set_text_in_labels()

    def mousePressEvent(self, event):
        print("click")
        self.clicked.emit()
        super().mousePressEvent(event)