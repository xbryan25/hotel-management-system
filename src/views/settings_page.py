from PyQt6.QtWidgets import QWidget

from ui import SettingsPageUI


class SettingsPage(QWidget, SettingsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
