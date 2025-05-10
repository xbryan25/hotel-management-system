from PyQt6.QtWidgets import QWidget, QTableView, QHeaderView
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, QModelIndex, Qt

from ui import BookingPageUI
from views.custom_widgets import DayFrame, ButtonDelegate, CustomTableView


class BookingPage(QWidget, BookingPageUI):
    clicked_info_button = pyqtSignal(QModelIndex)
    clicked_check_out_button = pyqtSignal(QModelIndex)

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.connect_signals_to_slots()

        self.update_table_view()

        self.set_external_stylesheet()
        self.load_fonts()

        self.set_table_views_button_delegate()
        self.disable_table_views_selection_mode()

    def update_table_view(self):
        # Remove old table view before adding

        for i in reversed(range(self.gridLayout_2.count())):
            item = self.gridLayout_2.itemAt(i)
            widget = item.widget()
            if widget and widget.objectName() == "bookings_table_view":
                self.gridLayout_2.removeWidget(widget)
                widget.setParent(None)

        self.bookings_table_view = CustomTableView(parent=self.bookings_table_view_frame, table_view_mode="bookings")

        self.gridLayout_2.addWidget(self.bookings_table_view, 0, 0, 1, 1)

    def set_table_views_column_widths(self):
        bookings_table_view_header = self.bookings_table_view.horizontalHeader()

        bookings_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFFFF;
                border: none;
                outline: none;
                padding-top: 10px;
            }
        """)

        bookings_table_view_header.resizeSection(0, 150)
        bookings_table_view_header.resizeSection(2, 105)
        bookings_table_view_header.resizeSection(3, 150)
        bookings_table_view_header.resizeSection(4, 220)
        bookings_table_view_header.resizeSection(5, 40)
        bookings_table_view_header.resizeSection(6, 40)

        bookings_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        bookings_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        bookings_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        bookings_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        bookings_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        bookings_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        bookings_table_view_header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)

    def set_table_views_button_delegate(self):
        info_button_delegate_icon_path = "../resources/icons/booking_page/info_icon.svg"
        self.info_button_delegate = ButtonDelegate(icon_path=info_button_delegate_icon_path,
                                                   can_be_disabled=False,
                                                   parent=self.bookings_table_view)

        self.info_button_delegate.clicked.connect(self.clicked_info_button.emit)
        self.bookings_table_view.setItemDelegateForColumn(5, self.info_button_delegate)

        check_out_button_delegate_icon_path = "../resources/icons/booking_page/check_out_icon.svg"
        self.check_out_button_delegate = ButtonDelegate(icon_path=check_out_button_delegate_icon_path,
                                                        can_be_disabled=True,
                                                        parent=self.bookings_table_view)

        self.check_out_button_delegate.clicked.connect(self.clicked_check_out_button.emit)
        self.bookings_table_view.setItemDelegateForColumn(6, self.check_out_button_delegate)

    def disable_table_views_selection_mode(self):
        self.bookings_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.bookings_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def connect_signals_to_slots(self):
        pass

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