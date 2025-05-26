from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtCore import QSize

from ui.list_rooms_frame_ui import Ui_Frame as ListRoomsFrameUI


class ListRoomsFrame(QFrame, ListRoomsFrameUI):
    def __init__(self, room_details):
        super().__init__()

        self.setupUi(self)

        self.room_details = room_details

        self.load_room_details()

        self.set_external_stylesheet()

        self.set_icons()
        self.load_fonts()

    def load_room_details(self):
        self.room_type_value_label.setText(self.room_details["room_type"])

    def set_external_stylesheet(self):
        with open("../resources/styles/list_rooms_frame.qss", "r") as file:
            self.setStyleSheet(file.read())

    def set_icons(self):
        self.edit_button.setIcon(QIcon("../resources/icons/edit_icon.svg"))
        self.edit_button.setIconSize(QSize(25, 25))

        self.delete_button.setIcon(QIcon("../resources/icons/delete_icon.svg"))
        self.delete_button.setIconSize(QSize(25, 25))

    def load_fonts(self):

        # day_and_time_frame
        self.room_num_label.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.room_type_value_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))

        self.capacity_value_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))

        self.rate_value_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))

        self.status_value_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))

    def set_status_value_label_stylesheet(self):

        value = self.status_value_label.text()

        if value == "Available":
            self.status_value_label.setStyleSheet("QLabel{color: #1FD100}")
        elif value == "Occupied":
            self.status_value_label.setStyleSheet("QLabel{color: #FF0000}")
        elif value == "Reserved":
            self.status_value_label.setStyleSheet("QLabel{color: #FFAD4E}")