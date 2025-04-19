from PyQt6.QtWidgets import QWidget

from ui.guests_page_ui import Ui_Widget as GuestsPageUI


class GuestsPage(QWidget, GuestsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
