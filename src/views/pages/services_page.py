from PyQt6.QtWidgets import QWidget, QHeaderView, QTableView, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QIcon, QIntValidator , QColor
from PyQt6.QtCore import QSize, QTimer, pyqtSignal, QModelIndex, Qt

from ui import ServicesPageUI
from views.custom_widgets import ButtonDelegate, CustomTableView


class ServicesPage(QWidget, ServicesPageUI):
    window_resized = pyqtSignal()
    clicked_add_service_button = pyqtSignal()
    clicked_edit_button = pyqtSignal(str, QModelIndex)
    clicked_change_active_status_button = pyqtSignal(QModelIndex)
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
        self.apply_shadow(self.service_table_view_frame)
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
            if widget and widget.objectName() == "services_table_view":
                self.gridLayout_2.removeWidget(widget)
                widget.setParent(None)

        self.services_table_view = CustomTableView(parent=self.service_table_view_frame, table_view_mode="services")

        self.gridLayout_2.addWidget(self.services_table_view, 0, 0, 1, 1)

    def set_table_views_column_widths(self):
        services_table_view_header = self.services_table_view.horizontalHeader()

        services_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFFFF;
                border: none;
                outline: none;
                padding-top: 10px; 
            }
        """)

        services_table_view_header.resizeSection(2, 150)
        services_table_view_header.resizeSection(3, 40)
        services_table_view_header.resizeSection(4, 40)

        # services_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        services_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        services_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        services_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        services_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)

    def set_table_views_button_delegate(self):

        edit_button_delegate_icon_path = "../resources/icons/edit_icon.svg"
        self.edit_button_delegate = ButtonDelegate(icon_path=edit_button_delegate_icon_path,
                                                   can_be_disabled=False,
                                                   parent=self.services_table_view)

        self.edit_button_delegate.clicked.connect(lambda index: self.clicked_edit_button.emit("edit_service", index))
        self.services_table_view.setItemDelegateForColumn(3, self.edit_button_delegate)

        delete_button_delegate_icon_path = "../resources/icons/delete_icon.svg"
        restore_button_delegate_icon_path = "../resources/icons/restore_icon.svg"
        self.change_active_status_button_delegate = ButtonDelegate(icon_path=delete_button_delegate_icon_path,
                                                                   can_be_disabled=False,
                                                                   parent=self.services_table_view,
                                                                   alt_icon_path=restore_button_delegate_icon_path)

        self.change_active_status_button_delegate.clicked.connect(self.clicked_change_active_status_button.emit)
        self.services_table_view.setItemDelegateForColumn(4, self.change_active_status_button_delegate)

    def disable_table_views_selection_mode(self):
        self.services_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.services_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def connect_signals_to_slots(self):
        self.add_service_button.clicked.connect(self.clicked_add_service_button.emit)

        self.search_lineedit.textChanged.connect(self.start_debounce_timer)
        self.timer.timeout.connect(self.on_debounced_text_changed)

        self.next_page_button.clicked.connect(self.next_page_button_pressed.emit)
        self.previous_page_button.clicked.connect(self.previous_page_button_pressed.emit)

        self.page_number_lineedit.textChanged.connect(self.page_number_lineedit_changed.emit)

    def get_max_rows_of_services_table_view(self):
        self.services_table_view.updateGeometry()
        QApplication.processEvents()

        viewport_height = self.services_table_view.viewport().height()

        if self.services_table_view.model() is None or self.services_table_view.model().rowCount() == 0:
            return 0

        # 2 is for buffer, to avoid the scroll bar showing up
        row_height = self.services_table_view.rowHeight(0)

        if row_height == 0:
            return 0

        max_rows = viewport_height // row_height

        self.services_table_view.updateGeometry()
        QApplication.processEvents()

        return max_rows

    def set_icons(self):
        self.add_service_button.setIcon(QIcon("../resources/icons/add_icon.svg"))
        self.add_service_button.setIconSize(QSize(20, 20))

    def set_external_stylesheet(self):
        with open("../resources/styles/services_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.services_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.view_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.add_service_button.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.services_table_view.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.services_table_view.horizontalHeader().setFont(QFont("Inter", 14, QFont.Weight.Bold))

        self.page_number_lineedit.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.of_page_number_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.window_resized.emit)