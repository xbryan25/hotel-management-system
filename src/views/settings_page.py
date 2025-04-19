from PyQt6.QtWidgets import QWidget

from ui.settings_page_ui import Ui_Widget as SettingsPageUI


class SettingsPage(QWidget, SettingsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
