from PyQt6.QtWidgets import QWidget, QSpacerItem, QSizePolicy

from custom_widgets.list_rooms_frame import ListRoomsFrame

from ui.rooms_page_ui import Ui_Widget as RoomsPageUI


class RoomsPage(QWidget, RoomsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.max_list_rooms_frame = 0

        self.make_list_view_rooms_frame()

    def make_list_view_rooms_frame(self):

        list_rooms_frame_height = 90

        new_max_list_rooms_frame = self.list_view_contents_frame.height() // list_rooms_frame_height

        if new_max_list_rooms_frame < self.max_list_rooms_frame:
            self.clear_list_view_frames(new_max_list_rooms_frame)

        elif new_max_list_rooms_frame > self.max_list_rooms_frame:
            for i in range(new_max_list_rooms_frame):
                item = self.gridLayout_8.itemAtPosition(i, 1)

                if item is None:
                    self.gridLayout_8.addWidget(ListRoomsFrame({"room_type": "single"}), i, 1, 1, 1)
                elif isinstance(item, QSpacerItem):
                    self.gridLayout_8.removeItem(item)
                    self.gridLayout_8.addWidget(ListRoomsFrame({"room_type": "single"}), i, 1, 1, 1)

        if new_max_list_rooms_frame != self.max_list_rooms_frame:
            self.max_list_rooms_frame = new_max_list_rooms_frame

            spacerItem14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.gridLayout_8.addItem(spacerItem14, self.max_list_rooms_frame, 1, 1, 1)

        print("Elements in grid layout: " + str(self.gridLayout_8.count()))

    def clear_list_view_frames(self, new_max_list_rooms_frame):
        for i in reversed(range(new_max_list_rooms_frame,self.gridLayout_8.count())):

            item = self.gridLayout_8.takeAt(i)

            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def resizeEvent(self, event):
        self.make_list_view_rooms_frame()

