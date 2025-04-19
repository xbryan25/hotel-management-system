from PyQt6.QtWidgets import QWidget

from ui.rooms_page_ui import Ui_Widget as RoomsPageUI


class RoomsPage(QWidget, RoomsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
