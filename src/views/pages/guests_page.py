from PyQt6.QtWidgets import QWidget, QHeaderView, QTableView, QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal, QModelIndex, QTimer

from ui import GuestsPageUI
from views.custom_widgets import ButtonDelegate, CustomTableView


class GuestsPage(QWidget, GuestsPageUI):
    window_resized = pyqtSignal()
    clicked_info_button = pyqtSignal(QModelIndex)
    search_text_changed = pyqtSignal(str)
    next_page_button_pressed = pyqtSignal()
    previous_page_button_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.update_table_view()

        self.disable_table_views_selection_mode()
        self.set_table_views_button_delegate()

        self.add_timer_to_search_lineedit()

        self.connect_signals_to_slots()

        self.set_external_stylesheet()
        self.load_fonts()

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
            if widget and widget.objectName() == "guest_table_view":
                self.gridLayout_2.removeWidget(widget)
                widget.setParent(None)

        self.guest_table_view = CustomTableView(parent=self.guest_table_view_frame, table_view_mode="guests")

        self.gridLayout_2.addWidget(self.guest_table_view, 0, 0, 1, 1)

    def set_table_views_column_widths(self):
        guest_table_view_header = self.guest_table_view.horizontalHeader()

        guest_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFFFF;
                color: #000000;
                border: none;
                outline: none;
            }
        """)

        # guest_table_view_header.resizeSection(0, 10)
        guest_table_view_header.resizeSection(2, 150)
        guest_table_view_header.resizeSection(3, 140)
        guest_table_view_header.resizeSection(4, 130)
        guest_table_view_header.resizeSection(5, 170)
        guest_table_view_header.resizeSection(6, 50)

        # guest_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        guest_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        guest_table_view_header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)

    def set_table_views_button_delegate(self):
        button_delegate_icon_path = "../resources/icons/guests_page/info_icon.svg"

        self.button_delegate = ButtonDelegate(icon_path=button_delegate_icon_path,
                                              can_be_disabled=False,
                                              parent=self.guest_table_view)

        self.guest_table_view.setItemDelegateForColumn(6, self.button_delegate)

    def connect_signals_to_slots(self):
        self.button_delegate.clicked.connect(self.clicked_info_button.emit)

        self.search_lineedit.textChanged.connect(self.start_debounce_timer)
        self.timer.timeout.connect(self.on_debounced_text_changed)

        self.next_page_button.clicked.connect(self.next_page_button_pressed.emit)
        self.previous_page_button.clicked.connect(self.previous_page_button_pressed.emit)

    def disable_table_views_selection_mode(self):
        self.guest_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.guest_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def get_max_rows_of_guest_table_view(self):
        self.guest_table_view.updateGeometry()
        QApplication.processEvents()

        viewport_height = self.guest_table_view.viewport().height()
        print(f"Viewport height: {viewport_height}")

        if self.guest_table_view.model() is None or self.guest_table_view.model().rowCount() == 0:
            return 0

        # if self.guest_table_view.model() is None:
        #     return 0

        # 2 is for buffer, to avoid the scroll bar showing up
        row_height = self.guest_table_view.rowHeight(0)
        print(f"Row height: {row_height}")

        if row_height == 0:
            return 0

        max_rows = viewport_height // row_height
        print(f"Max rows that can fit: {max_rows}")

        self.guest_table_view.updateGeometry()
        QApplication.processEvents()

        return max_rows

    def set_external_stylesheet(self):
        with open("../resources/styles/guests_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.guest_list_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.show_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.guest_table_view.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.guest_table_view.horizontalHeader().setFont(QFont("Inter", 14, QFont.Weight.Bold))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.window_resized.emit)
