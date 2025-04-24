from PyQt6.QtWidgets import QWidget, QHeaderView
from PyQt6.QtGui import QFont

from ui.dashboard_page_ui import Ui_Widget as DashboardPageUI


class DashboardPage(QWidget, DashboardPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

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

        reservation_list_frame_table_view_header.resizeSection(0, 95)
        reservation_list_frame_table_view_header.resizeSection(2, 75)
        reservation_list_frame_table_view_header.resizeSection(3, 95)
        reservation_list_frame_table_view_header.resizeSection(4, 155)
        reservation_list_frame_table_view_header.resizeSection(5, 65)

        reservation_list_frame_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        reservation_list_frame_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        reservation_list_frame_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        reservation_list_frame_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        reservation_list_frame_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        reservation_list_frame_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

    def set_external_stylesheet(self):
        with open("../resources/styles/dashboard_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        # day_and_time_frame
        self.current_day_label.setFont(QFont("Inter", 16, QFont.Weight.Light))
        self.current_time_label.setFont(QFont("Inter", 26, QFont.Weight.ExtraBold))

        # search_bar_frame
        self.search_bar_frame_search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

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

        self.recent_check_in_frame_label.setFont(QFont("Inter", 14, QFont.Weight.ExtraBold))
        # self.aw.recent_check_in_frame_table_widget.horizontalHeader().setFont(QFont(self.inter_font_family, 14, QFont.Weight.ExtraBold))

        self.recent_check_out_frame_label.setFont(QFont("Inter", 14, QFont.Weight.ExtraBold))
        # self.aw.recent_check_out_frame_table_widget.horizontalHeader().setFont(QFont(self.inter_font_family, 14, QFont.Weight.ExtraBold))

        # reservation_list_frame
        self.reservation_list_frame_label.setFont(QFont("Inter", 16, QFont.Weight.ExtraBold))
        self.reservation_list_frame_add_reservation_button.setFont(
            QFont("Inter", 10, QFont.Weight.Normal))
        self.reservation_list_frame_search_lineedit.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.reservation_list_frame_status_combobox.setFont(QFont("Inter", 10, QFont.Weight.Normal))

        # quick_action_frame
        self.quick_action_frame_label.setFont(QFont("Inter", 16, QFont.Weight.ExtraBold))

        self.quick_action_frame_check_in_button.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.quick_action_frame_check_out_button.setFont(QFont("Inter", 10, QFont.Weight.Normal))

        self.quick_action_frame_room_num_label.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.quick_action_frame_room_num_lineedit.setFont(QFont("Inter", 10, QFont.Weight.Normal))

        self.quick_action_frame_guest_name_label.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.quick_action_frame_guest_name_lineedit.setFont(QFont("Inter", 10, QFont.Weight.Normal))

        self.quick_action_frame_cancel_button.setFont(QFont("Inter", 10, QFont.Weight.Normal))
        self.quick_action_frame_confirm_button.setFont(QFont("Inter", 10, QFont.Weight.Normal))

        # rooms_frame
        self.rooms_frame_label.setFont(QFont("Inter", 16, QFont.Weight.ExtraBold))

        self.rooms_frame_status_combobox.setFont(QFont("Inter", 10, QFont.Weight.Normal))