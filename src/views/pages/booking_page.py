from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QFont

from ui import BookingPageUI


class BookingPage(QWidget, BookingPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

    def set_external_stylesheet(self):
        with open("../resources/styles/booking_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.bookings_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))
        self.date_today_label.setFont(QFont("Inter", 18, QFont.Weight.Normal))

        self.view_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.bookings_table_view.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.bookings_table_view.horizontalHeader().setFont(QFont("Inter", 14, QFont.Weight.Bold))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))