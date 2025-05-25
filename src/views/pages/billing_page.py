from PyQt6.QtWidgets import QWidget, QTableView, QHeaderView, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QIntValidator, QColor
from PyQt6.QtCore import pyqtSignal, QModelIndex, Qt, QTimer

from ui import BillingPageUI
from views.custom_widgets import DayFrame, ButtonDelegate, CustomTableView


class BillingPage(QWidget, BillingPageUI):
    window_resized = pyqtSignal()
    clicked_add_payment_button = pyqtSignal(QModelIndex)
    search_text_changed = pyqtSignal(str)
    next_page_button_pressed = pyqtSignal()
    previous_page_button_pressed = pyqtSignal()
    page_number_lineedit_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.add_timer_to_search_lineedit()
        self.connect_signals_to_slots()

        self.update_table_view()

        self.set_table_views_button_delegate()
        self.disable_table_views_selection_mode()

        self.set_external_stylesheet()
        self.load_fonts()

        self.apply_shadow_to_frames()

    @staticmethod
    def apply_shadow(widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)

    def apply_shadow_to_frames(self):
        self.apply_shadow(self.billings_table_view_frame)
        self.apply_shadow(self.actions_frame)

    def update_of_page_number_label(self, total_pages):
        total_pages = max(total_pages, 1)

        self.of_page_number_label.setText(f"of {total_pages}")

    def set_page_number_lineedit_validator(self, total_pages):
        validator = QIntValidator(1, total_pages)
        self.page_number_lineedit.setValidator(validator)

    def add_timer_to_search_lineedit(self):
        self.timer = QTimer()

        self.timer.setInterval(300)
        self.timer.setSingleShot(True)

    def start_debounce_timer(self):
        self.timer.start()

    def on_debounced_text_changed(self):
        self.search_text_changed.emit(self.search_lineedit.text())

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

    def connect_signals_to_slots(self):
        self.search_lineedit.textChanged.connect(self.start_debounce_timer)
        self.timer.timeout.connect(self.on_debounced_text_changed)

        self.next_page_button.clicked.connect(self.next_page_button_pressed.emit)
        self.previous_page_button.clicked.connect(self.previous_page_button_pressed.emit)

        self.page_number_lineedit.textChanged.connect(self.page_number_lineedit_changed.emit)

    def get_max_rows_of_billings_table_view(self):
        self.billings_table_view.updateGeometry()
        QApplication.processEvents()

        viewport_height = self.billings_table_view.viewport().height()

        if self.billings_table_view.model() is None or self.billings_table_view.model().rowCount() == 0:
            return 0

        # 2 is for buffer, to avoid the scroll bar showing up
        row_height = self.billings_table_view.rowHeight(0)

        if row_height == 0:
            return 0

        max_rows = viewport_height // row_height

        self.billings_table_view.updateGeometry()
        QApplication.processEvents()

        return max_rows

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

        self.page_number_lineedit.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.of_page_number_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.window_resized.emit)
