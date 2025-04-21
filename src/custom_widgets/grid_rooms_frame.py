from PyQt6.QtWidgets import QFrame

from ui.grid_rooms_frame_ui import Ui_Frame as GridRoomsFrameUI


class GridRoomsFrame(QFrame, GridRoomsFrameUI):
    def __init__(self, room_details):
        super().__init__()

        self.setupUi(self)

        self.room_details = room_details

        self.load_room_details()

    def load_room_details(self):
        self.room_num_and_title_label.setText(self.room_details["room_type"])
