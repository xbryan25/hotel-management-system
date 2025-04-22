from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtCore import QSize

from ui.grid_rooms_frame_ui import Ui_Frame as GridRoomsFrameUI


class GridRoomsFrame(QFrame, GridRoomsFrameUI):
    def __init__(self, room_details):
        super().__init__()

        self.setupUi(self)

        self.room_details = room_details

        self.load_room_details()

        self.set_external_stylesheet()

        self.set_icons()
        self.load_fonts()

        self.set_status_value_label_stylesheet("available")

    def load_room_details(self):
        self.room_num_and_title_label.setText(self.room_details["room_type"])

    def set_external_stylesheet(self):
        with open("../resources/styles/grid_rooms_frame.qss", "r") as file:
            self.setStyleSheet(file.read())

    def set_icons(self):
        self.edit_button.setIcon(QIcon("../resources/icons/custom_widgets/edit_icon.svg"))
        self.edit_button.setIconSize(QSize(20, 20))

        self.delete_button.setIcon(QIcon("../resources/icons/custom_widgets/delete_icon.svg"))
        self.delete_button.setIconSize(QSize(20, 20))

    def load_fonts(self):
        # day_and_time_frame
        self.room_num_and_title_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

        self.capacity_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

        self.rate_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))
        self.actual_rate_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

        self.status_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))
        self.actual_status_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

        self.actions_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

    def set_status_value_label_stylesheet(self, value):

        if value == "available":
            self.actual_status_label.setStyleSheet("QLabel{color: #1FD100}")
        elif value == "occupied":
            self.actual_status_label.setStyleSheet("QLabel{color: #FF0000}")
        elif value == "reserved":
            self.actual_status_label.setStyleSheet("QLabel{color: #FFAD4E}")