from PyQt6.QtWidgets import QWidget, QHeaderView
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QSize

from ui import ServicesPageUI


class ServicesPage(QWidget, ServicesPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.set_icons()

    def set_table_views_column_widths(self):
        services_table_view_header = self.services_table_view.horizontalHeader()

        services_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFFFF;
                border: none;
                outline: none;
            }
        """)

        services_table_view_header.resizeSection(1, 250)

        services_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        services_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)


    def set_icons(self):
        self.add_service_button.setIcon(QIcon("../resources/icons/services_page/add_icon.svg"))
        self.add_service_button.setIconSize(QSize(20, 20))

    def set_external_stylesheet(self):
        with open("../resources/styles/services_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.services_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.add_service_button.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.services_table_view.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.services_table_view.horizontalHeader().setFont(QFont("Inter", 14, QFont.Weight.Bold))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
