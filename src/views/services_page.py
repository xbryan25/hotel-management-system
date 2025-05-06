from PyQt6.QtWidgets import QWidget

from ui import ServicesPageUI


class ServicesPage(QWidget, ServicesPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
