from PyQt6.QtWidgets import QWidget

from ui.services_page_ui import Ui_Widget as ServicesPageUI


class ServicesPage(QWidget, ServicesPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
