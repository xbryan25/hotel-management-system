from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtCore import QSize

from ui.grid_rooms_frame_ui import Ui_Frame as GridRoomsFrameUI


class GridRoomsFrame(QFrame, GridRoomsFrameUI):
    def __init__(self, room_details):
        super().__init__()

        self.setupUi(self)

        self.room_details = room_details

        # self.load_room_details()

        self.set_external_stylesheet()

        self.set_icons()
        self.load_fonts()

    def set_room_num_and_title_label(self, room_num, room_type):
        self.room_num_and_title_label.setText(f"{room_num} - {self.truncate_text(room_type)}")
        self.room_num_and_title_label.setToolTip(room_type)

    @staticmethod
    def truncate_text(text, max_length=12):
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    def set_external_stylesheet(self):
        with open("../resources/styles/grid_rooms_frame.qss", "r") as file:
            self.setStyleSheet(file.read())

    def set_icons(self):
        self.edit_button.setIcon(QIcon("../resources/icons/edit_icon.svg"))
        self.edit_button.setIconSize(QSize(20, 20))

        self.delete_button.setIcon(QIcon("../resources/icons/delete_icon.svg"))
        self.delete_button.setIconSize(QSize(20, 20))

    def load_fonts(self):
        # day_and_time_frame
        self.room_num_and_title_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

        self.capacity_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

        self.rate_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))
        self.rate_value_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

        self.status_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))
        self.status_value_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

        self.actions_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

    def set_status_value_label_stylesheet(self):

        value = self.status_value_label.text()

        if value == "Available":
            self.status_value_label.setStyleSheet("QLabel{color: #1FD100}")
        elif value == "Occupied":
            self.status_value_label.setStyleSheet("QLabel{color: #FF0000}")
        elif value == "Reserved":
            self.status_value_label.setStyleSheet("QLabel{color: #FFAD4E}")