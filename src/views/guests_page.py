from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QFont

from ui.guests_page_ui import Ui_Widget as GuestsPageUI


class GuestsPage(QWidget, GuestsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.load_fonts()

    def set_external_stylesheet(self):
        with open("../resources/styles/guests_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.guest_list_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))