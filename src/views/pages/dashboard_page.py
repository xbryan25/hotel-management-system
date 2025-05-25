from PyQt6.QtWidgets import QWidget, QHeaderView, QTableView, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, pyqtSignal

from ui import DashboardPageUI


class DashboardPage(QWidget, DashboardPageUI):
    changed_reservations_combobox = pyqtSignal(str)
    changed_room_status = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.connect_signals_to_slots()

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

        self.apply_shadow(self.today_check_in_frame)
        self.apply_shadow(self.today_check_out_frame)
        self.apply_shadow(self.available_rooms_frame)
        self.apply_shadow(self.reserved_rooms_frame)
        self.apply_shadow(self.booked_rooms_frame)
        self.apply_shadow(self.todays_activity_frame)
        self.apply_shadow(self.reservation_list_frame)
        self.apply_shadow(self.rooms_frame)

    def connect_signals_to_slots(self):
        self.reservations_combobox.currentTextChanged.connect(self.changed_reservations_combobox.emit)
        self.rooms_frame_status_combobox.currentTextChanged.connect(self.changed_room_status.emit)

    def disable_table_views_selection_mode(self):
        self.recent_check_in_frame_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.recent_check_in_frame_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.recent_check_out_frame_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.recent_check_out_frame_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.reservation_list_frame_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.reservation_list_frame_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.rooms_frame_table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.rooms_frame_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_table_views_column_widths(self):
        recent_check_in_frame_table_view_header = self.recent_check_in_frame_table_view.horizontalHeader()

        recent_check_in_frame_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #E3F2FD;
                border: none;
                outline: none;
            }
        """)

        recent_check_in_frame_table_view_header.resizeSection(0, 85)
        recent_check_in_frame_table_view_header.resizeSection(2, 75)
        recent_check_in_frame_table_view_header.resizeSection(3, 65)

        recent_check_in_frame_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        recent_check_in_frame_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        recent_check_in_frame_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        recent_check_in_frame_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)

        recent_check_out_frame_table_view_header = self.recent_check_out_frame_table_view.horizontalHeader()

        recent_check_out_frame_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFF3E0;
                border: none;
                outline: none;
            }
        """)

        recent_check_out_frame_table_view_header.resizeSection(0, 85)
        recent_check_out_frame_table_view_header.resizeSection(2, 75)
        recent_check_out_frame_table_view_header.resizeSection(3, 65)

        recent_check_out_frame_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        recent_check_out_frame_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        recent_check_out_frame_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        recent_check_out_frame_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)

        reservation_list_frame_table_view_header = self.reservation_list_frame_table_view.horizontalHeader()

        reservation_list_frame_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFFFF;
                border: none;
                outline: none;
            }
        """)

        reservation_list_frame_table_view_header.resizeSection(0, 115)
        reservation_list_frame_table_view_header.resizeSection(2, 80)
        reservation_list_frame_table_view_header.resizeSection(3, 100)
        reservation_list_frame_table_view_header.resizeSection(4, 185)
        reservation_list_frame_table_view_header.resizeSection(5, 90)

        reservation_list_frame_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        reservation_list_frame_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        reservation_list_frame_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        reservation_list_frame_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        reservation_list_frame_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        reservation_list_frame_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

        rooms_frame_table_view_header = self.rooms_frame_table_view.horizontalHeader()

        rooms_frame_table_view_header.setStyleSheet("""
                    QHeaderView::section {
                        background-color: #FFFFFF;
                        border: none;
                        outline: none;
                    }
                """)

        rooms_frame_table_view_header.resizeSection(0, 100)

        rooms_frame_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        rooms_frame_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def set_external_stylesheet(self):
        with open("../resources/styles/dashboard_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        # day_and_time_frame
        self.current_day_label.setFont(QFont("Inter", 16, QFont.Weight.Light))
        self.current_time_label.setFont(QFont("Inter", 26, QFont.Weight.ExtraBold))

        # overview_frame
        self.overview_label.setFont(QFont("Inter", 16, QFont.Weight.ExtraBold))

        self.today_check_in_frame_top_label.setFont(QFont("Inter", 13, QFont.Weight.Light))
        self.today_check_in_frame_bottom_label.setFont(QFont("Inter", 13, QFont.Weight.ExtraBold))
        self.today_check_in_frame_num_label.setFont(QFont("Inter", 26, QFont.Weight.ExtraBold))

        self.today_check_out_frame_top_label.setFont(QFont("Inter", 13, QFont.Weight.Light))
        self.today_check_out_frame_bottom_label.setFont(QFont("Inter", 13, QFont.Weight.ExtraBold))
        self.today_check_out_frame_num_label.setFont(QFont("Inter", 26, QFont.Weight.ExtraBold))

        self.available_rooms_frame_top_label.setFont(QFont("Inter", 13, QFont.Weight.Light))
        self.available_rooms_frame_bottom_label.setFont(QFont("Inter", 13, QFont.Weight.ExtraBold))
        self.available_rooms_frame_num_label.setFont(QFont("Inter", 26, QFont.Weight.ExtraBold))

        self.reserved_rooms_frame_top_label.setFont(QFont("Inter", 13, QFont.Weight.Light))
        self.reserved_rooms_frame_bottom_label.setFont(QFont("Inter", 13, QFont.Weight.ExtraBold))
        self.reserved_rooms_frame_num_label.setFont(QFont("Inter", 26, QFont.Weight.ExtraBold))

        self.booked_rooms_frame_top_label.setFont(QFont("Inter", 13, QFont.Weight.Light))
        self.booked_rooms_frame_bottom_label.setFont(QFont("Inter", 13, QFont.Weight.ExtraBold))
        self.booked_rooms_frame_num_label.setFont(QFont("Inter", 26, QFont.Weight.ExtraBold))

        # todays_activity_frame
        self.todays_activity_frame_label.setFont(QFont("Inter", 16, QFont.Weight.ExtraBold))

        self.recent_check_in_frame_label.setFont(QFont("Inter", 15, QFont.Weight.ExtraBold))
        self.recent_check_in_frame_table_view.setFont(QFont("Inter", 9, QFont.Weight.Normal))
        self.recent_check_in_frame_table_view.horizontalHeader().setFont(QFont("Inter", 12, QFont.Weight.DemiBold))

        self.recent_check_out_frame_label.setFont(QFont("Inter", 15, QFont.Weight.ExtraBold))
        self.recent_check_out_frame_table_view.setFont(QFont("Inter", 9, QFont.Weight.Normal))
        self.recent_check_out_frame_table_view.horizontalHeader().setFont(QFont("Inter", 12, QFont.Weight.DemiBold))

        # reservation_list_frame
        self.next_label.setFont(QFont("Inter", 16, QFont.Weight.ExtraBold))
        self.reservations_combobox.setFont(QFont("Inter", 16, QFont.Weight.ExtraBold))
        self.reservations_label.setFont(QFont("Inter", 16, QFont.Weight.ExtraBold))
        self.reservation_list_frame_table_view.setFont(QFont("Inter", 9, QFont.Weight.Normal))
        self.reservation_list_frame_table_view.horizontalHeader().setFont(QFont("Inter", 12, QFont.Weight.DemiBold))

        # rooms_frame
        self.rooms_frame_label.setFont(QFont("Inter", 16, QFont.Weight.ExtraBold))
        self.rooms_frame_status_combobox.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.rooms_frame_table_view.setFont(QFont("Inter", 9, QFont.Weight.Normal))
        self.rooms_frame_table_view.horizontalHeader().setFont(QFont("Inter", 12, QFont.Weight.DemiBold))
