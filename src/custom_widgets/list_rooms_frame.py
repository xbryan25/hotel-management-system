from PyQt6.QtWidgets import QFrame

from ui.list_rooms_frame_ui import Ui_Frame as ListRoomsFrameUI


class ListRoomsFrame(QFrame, ListRoomsFrameUI):
    def __init__(self, room_details):
        super().__init__()

        self.setupUi(self)

        self.room_details = room_details

        self.load_room_details()

    def load_room_details(self):
        self.room_type_value_label.setText(self.room_details["room_type"])
