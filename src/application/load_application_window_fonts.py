from PyQt6.QtGui import QFont, QFontDatabase


class LoadApplicationWindowFonts:
    def __init__(self, application_window):
        self.aw = application_window

        self.inter_font_family = self.aw.inter_font_family

    def load_fonts(self):
        self.load_sidebar_fonts()
        self.load_dashboard_page_fonts()

    def load_sidebar_fonts(self):
        self.aw.expanded_buttons_list_widget.setFont(QFont(self.inter_font_family, 14, QFont.Weight.Medium))

    def load_dashboard_page_fonts(self):
        # day_and_time_frame
        self.aw.current_day_label.setFont(QFont(self.inter_font_family, 16, QFont.Weight.Light))
        self.aw.current_time_label.setFont(QFont(self.inter_font_family, 26, QFont.Weight.ExtraBold))

        # search_bar_frame
        self.aw.search_bar_frame_search_lineedit.setFont(QFont(self.inter_font_family, 16, QFont.Weight.Light))

        # overview_frame
        self.aw.overview_label.setFont(QFont(self.inter_font_family, 16, QFont.Weight.ExtraBold))

        self.aw.today_check_in_frame_top_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.Light))
        self.aw.today_check_in_frame_bottom_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.ExtraBold))
        self.aw.today_check_in_frame_num_label.setFont(QFont(self.inter_font_family, 26, QFont.Weight.ExtraBold))

        self.aw.today_check_out_frame_top_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.Light))
        self.aw.today_check_out_frame_bottom_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.ExtraBold))
        self.aw.today_check_out_frame_num_label.setFont(QFont(self.inter_font_family, 26, QFont.Weight.ExtraBold))

        self.aw.available_rooms_frame_top_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.Light))
        self.aw.available_rooms_frame_bottom_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.ExtraBold))
        self.aw.available_rooms_frame_num_label.setFont(QFont(self.inter_font_family, 26, QFont.Weight.ExtraBold))

        self.aw.reserved_rooms_frame_top_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.Light))
        self.aw.reserved_rooms_frame_bottom_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.ExtraBold))
        self.aw.reserved_rooms_frame_num_label.setFont(QFont(self.inter_font_family, 26, QFont.Weight.ExtraBold))

        self.aw.booked_rooms_frame_top_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.Light))
        self.aw.booked_rooms_frame_bottom_label.setFont(QFont(self.inter_font_family, 13, QFont.Weight.ExtraBold))
        self.aw.booked_rooms_frame_num_label.setFont(QFont(self.inter_font_family, 26, QFont.Weight.ExtraBold))

        # todays_activity_frame
        self.aw.todays_activity_frame_label.setFont(QFont(self.inter_font_family, 16, QFont.Weight.ExtraBold))

        self.aw.recent_check_in_frame_label.setFont(QFont(self.inter_font_family, 14, QFont.Weight.ExtraBold))
        # self.aw.recent_check_in_frame_table_widget.horizontalHeader().setFont(QFont(self.inter_font_family, 14, QFont.Weight.ExtraBold))

        self.aw.recent_check_out_frame_label.setFont(QFont(self.inter_font_family, 14, QFont.Weight.ExtraBold))
        # self.aw.recent_check_out_frame_table_widget.horizontalHeader().setFont(QFont(self.inter_font_family, 14, QFont.Weight.ExtraBold))

        # reservation_list_frame
        self.aw.reservation_list_frame_label.setFont(QFont(self.inter_font_family, 16, QFont.Weight.ExtraBold))
        self.aw.reservation_list_frame_add_reservation_button.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))
        self.aw.reservation_list_frame_search_lineedit.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))
        self.aw.reservation_list_frame_status_combobox.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))

        # quick_action_frame
        self.aw.quick_action_frame_label.setFont(QFont(self.inter_font_family, 16, QFont.Weight.ExtraBold))

        self.aw.quick_action_frame_check_in_button.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))
        self.aw.quick_action_frame_check_out_button.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))

        self.aw.quick_action_frame_room_num_label.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))
        self.aw.quick_action_frame_room_num_lineedit.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))

        self.aw.quick_action_frame_guest_name_label.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))
        self.aw.quick_action_frame_guest_name_lineedit.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))

        self.aw.quick_action_frame_cancel_button.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))
        self.aw.quick_action_frame_confirm_button.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))

        # rooms_frame
        self.aw.rooms_frame_label.setFont(QFont(self.inter_font_family, 16, QFont.Weight.ExtraBold))

        self.aw.rooms_frame_status_combobox.setFont(QFont(self.inter_font_family, 10, QFont.Weight.Normal))

