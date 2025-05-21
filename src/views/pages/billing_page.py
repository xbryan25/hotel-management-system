from PyQt6.QtWidgets import QWidget, QTableView, QHeaderView
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, QModelIndex, Qt

from ui import BillingPageUI
from views.custom_widgets import DayFrame, ButtonDelegate, CustomTableView


class BillingPage(QWidget, BillingPageUI):
    clicked_add_payment_button = pyqtSignal(QModelIndex)
    # clicked_check_out_button = pyqtSignal(QModelIndex)

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # self.connect_signals_to_slots()

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
            if widget and widget.objectName() == "billings_table_view":
                self.gridLayout_2.removeWidget(widget)
                widget.setParent(None)

        self.billings_table_view = CustomTableView(parent=self.billings_table_view_frame, table_view_mode="billings")

        self.gridLayout_2.addWidget(self.billings_table_view, 0, 0, 1, 1)

    def set_table_views_column_widths(self):
        billings_table_view_header = self.billings_table_view.horizontalHeader()

        billings_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFFFF;
                border: none;
                outline: none;
                padding-top: 10px;
            }
        """)

        billings_table_view_header.resizeSection(0, 150)
        billings_table_view_header.resizeSection(2, 105)
        billings_table_view_header.resizeSection(3, 250)
        billings_table_view_header.resizeSection(4, 100)
        billings_table_view_header.resizeSection(5, 40)

        billings_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        billings_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        billings_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        billings_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        billings_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        billings_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

    def set_table_views_button_delegate(self):
        payment_button_delegate_icon_path = "../resources/icons/billing_page/payment_icon.svg"
        self.payment_button_delegate = ButtonDelegate(icon_path=payment_button_delegate_icon_path,
                                                      can_be_disabled=True,
                                                      parent=self.billings_table_view)

        self.payment_button_delegate.clicked.connect(self.clicked_add_payment_button.emit)
        self.billings_table_view.setItemDelegateForColumn(5, self.payment_button_delegate)

    def disable_table_views_selection_mode(self):
        self.billings_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.billings_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    # def connect_signals_to_slots(self):
    #     pass

    def set_external_stylesheet(self):
        with open("../resources/styles/billing_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.billings_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.view_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.billings_table_view.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.billings_table_view.horizontalHeader().setFont(QFont("Inter", 14, QFont.Weight.Bold))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))