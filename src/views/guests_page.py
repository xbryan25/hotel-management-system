from PyQt6.QtWidgets import QWidget, QHeaderView, QTableView
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from ui.guests_page_ui import Ui_Widget as GuestsPageUI
from custom_widgets import ButtonDelegate, GuestTableView


class GuestsPage(QWidget, GuestsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.update_table_view()

        self.disable_table_views_selection_mode()
        self.set_table_views_button_delegate()

        self.set_external_stylesheet()

        self.load_fonts()

    def update_table_view(self):
        self.guest_table_view = GuestTableView(parent=self.guest_table_view_frame)

        self.gridLayout_2.addWidget(self.guest_table_view, 0, 0, 1, 1)

    def set_table_views_column_widths(self):
        guest_table_view_header = self.guest_table_view.horizontalHeader()

        guest_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFFFF;
                border: none;
                outline: none;
            }
        """)

        guest_table_view_header.resizeSection(1, 105)
        guest_table_view_header.resizeSection(2, 150)
        guest_table_view_header.resizeSection(3, 150)
        guest_table_view_header.resizeSection(4, 150)
        guest_table_view_header.resizeSection(5, 115)
        guest_table_view_header.resizeSection(6, 45)

        guest_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        guest_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)

    def set_table_views_button_delegate(self):
        self.button_delegate = ButtonDelegate(self.guest_table_view)
        self.button_delegate.clicked.connect(lambda: print("Info button clicked"))

        self.guest_table_view.setItemDelegateForColumn(6, self.button_delegate)

    def disable_table_views_selection_mode(self):
        self.guest_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.guest_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_external_stylesheet(self):
        with open("../resources/styles/guests_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.guest_list_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.guest_table_view.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.guest_table_view.horizontalHeader().setFont(QFont("Inter", 14, QFont.Weight.Bold))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))