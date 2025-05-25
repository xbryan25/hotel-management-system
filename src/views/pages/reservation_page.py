from PyQt6.QtCore import QTime, QTimer, QSize, Qt, pyqtSignal, QModelIndex
from PyQt6.QtWidgets import QWidget, QFrame, QHeaderView, QTableView, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QIcon, QIntValidator, QColor

from ui import ReservationPageUI
from views.custom_widgets import DayFrame, ButtonDelegate, CustomTableView

from datetime import date, timedelta


class ReservationPage(QWidget, ReservationPageUI):
    window_resized = pyqtSignal()
    clicked_add_reservation_button = pyqtSignal()
    clicked_info_button = pyqtSignal(QModelIndex)
    clicked_check_in_button = pyqtSignal(QModelIndex)
    search_text_changed = pyqtSignal(str)
    next_page_button_pressed = pyqtSignal()
    previous_page_button_pressed = pyqtSignal()
    page_number_lineedit_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.is_widget_shown = False

        # Days from left_most_day
        self.day_difference = 0
        self.left_most_day = date.today()
        self.selected_day = date.today()

        self.add_timer_to_search_lineedit()
        self.connect_signals_to_slots()

        self.update_table_view()

        self.set_icons()

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
        self.apply_shadow(self.reservations_table_view_frame)
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
            if widget and widget.objectName() == "reservations_table_view":
                self.gridLayout_2.removeWidget(widget)
                widget.setParent(None)

        self.reservations_table_view = CustomTableView(parent=self.reservations_table_view_frame, table_view_mode="reservations")

        self.gridLayout_2.addWidget(self.reservations_table_view, 0, 0, 1, 1)

    def set_table_views_column_widths(self):
        reservations_table_view_header = self.reservations_table_view.horizontalHeader()

        reservations_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFFFF;
                border: none;
                outline: none;
                padding-top: 5px;
            }
        """)

        reservations_table_view_header.resizeSection(0, 150)
        reservations_table_view_header.resizeSection(2, 105)
        reservations_table_view_header.resizeSection(3, 150)
        reservations_table_view_header.resizeSection(4, 220)
        reservations_table_view_header.resizeSection(5, 125)
        reservations_table_view_header.resizeSection(6, 40)
        reservations_table_view_header.resizeSection(7, 40)

        reservations_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        reservations_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)

    def set_table_views_button_delegate(self):
        info_button_delegate_icon_path = "../resources/icons/reservation_page/info_icon.svg"
        self.info_button_delegate = ButtonDelegate(icon_path=info_button_delegate_icon_path,
                                                   can_be_disabled=False,
                                                   parent=self.reservations_table_view)

        self.info_button_delegate.clicked.connect(self.clicked_info_button.emit)
        self.reservations_table_view.setItemDelegateForColumn(6, self.info_button_delegate)

        check_in_button_delegate_icon_path = "../resources/icons/reservation_page/check_in_icon.svg"
        self.check_in_button_delegate = ButtonDelegate(icon_path=check_in_button_delegate_icon_path,
                                                       can_be_disabled=True,
                                                       parent=self.reservations_table_view)

        self.check_in_button_delegate.clicked.connect(self.clicked_check_in_button.emit)
        self.reservations_table_view.setItemDelegateForColumn(7, self.check_in_button_delegate)

    def disable_table_views_selection_mode(self):
        self.reservations_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.reservations_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def connect_signals_to_slots(self):
        self.add_reservation_button.clicked.connect(self.clicked_add_reservation_button.emit)

        self.search_lineedit.textChanged.connect(self.start_debounce_timer)
        self.timer.timeout.connect(self.on_debounced_text_changed)

        self.next_page_button.clicked.connect(self.next_page_button_pressed.emit)
        self.previous_page_button.clicked.connect(self.previous_page_button_pressed.emit)

        self.page_number_lineedit.textChanged.connect(self.page_number_lineedit_changed.emit)

    def get_max_rows_of_reservations_table_view(self):
        self.reservations_table_view.updateGeometry()
        QApplication.processEvents()

        viewport_height = self.reservations_table_view.viewport().height()

        if self.reservations_table_view.model() is None or self.reservations_table_view.model().rowCount() == 0:
            return 0

        # 2 is for buffer, to avoid the scroll bar showing up
        row_height = self.reservations_table_view.rowHeight(0)

        if row_height == 0:
            return 0

        max_rows = viewport_height // row_height

        self.reservations_table_view.updateGeometry()
        QApplication.processEvents()

        return max_rows

    def set_external_stylesheet(self):
        with open("../resources/styles/reservation_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def set_icons(self):
        self.add_reservation_button.setIcon(QIcon("../resources/icons/reservation_page/add_icon.svg"))
        self.add_reservation_button.setIconSize(QSize(20, 20))

    def load_fonts(self):
        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.reservations_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.view_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.reservations_table_view.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.reservations_table_view.horizontalHeader().setFont(QFont("Inter", 14, QFont.Weight.Bold))

        self.add_reservation_button.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.page_number_lineedit.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.of_page_number_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.window_resized.emit)
