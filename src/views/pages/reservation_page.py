from PyQt6.QtCore import QTime, QTimer, QSize
from PyQt6.QtWidgets import QWidget, QFrame, QHeaderView
from PyQt6.QtGui import QFont, QIcon

from ui import ReservationPageUI

from views.custom_widgets import DayFrame

from datetime import date, timedelta


class ReservationPage(QWidget, ReservationPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.is_widget_shown = False

        # Days from left_most_day
        self.day_difference = 0
        self.left_most_day = date.today()
        self.selected_day = date.today()

        self.connect_signals_to_slots()

        self.set_icons()
        self.set_external_stylesheet()
        self.load_fonts()

        self.update_selected_day(self.left_most_day)
        self.update_selected_date_label(self.left_most_day)

    def set_table_views_column_widths(self):
        reservations_table_view_header = self.reservations_table_view.horizontalHeader()

        reservations_table_view_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFFFF;
                border: none;
                outline: none;
                padding-top: 10px;
            }
        """)

        reservations_table_view_header.resizeSection(0, 130)
        reservations_table_view_header.resizeSection(2, 105)
        reservations_table_view_header.resizeSection(3, 150)
        reservations_table_view_header.resizeSection(4, 200)
        reservations_table_view_header.resizeSection(5, 150)

        reservations_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        reservations_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        reservations_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

    def connect_signals_to_slots(self):
        self.reset_button.clicked.connect(lambda: self.update_day_frames("reset"))
        self.left_button.clicked.connect(lambda: self.update_day_frames("previous"))
        self.right_button.clicked.connect(lambda: self.update_day_frames("next"))

    def update_selected_date_label(self, selected_date):
        self.selected_date_label.setText(selected_date.strftime("%b %d, %Y"))

    def update_selected_day(self, selected_date):
        self.selected_day = selected_date

    def update_day_frames(self, direction):

        if direction == "previous":
            self.left_most_day = self.left_most_day - timedelta(days=self.sections_frame_h_layout.count())
        elif direction == "next":
            self.left_most_day = self.left_most_day + timedelta(days=self.sections_frame_h_layout.count())
        elif direction == "reset":
            self.left_most_day = date.today()

        for i in range(self.sections_frame_h_layout.count()):
            item = self.sections_frame_h_layout.itemAt(i)
            widget = item.widget()

            if isinstance(widget, QFrame):
                widget.update_current_date(self.left_most_day + timedelta(days=i))

        self.update_selected_date_label(self.left_most_day)

    def initialize_left_most_day(self, left_most_day):
        self.left_most_day = left_most_day

    def load_day_frames(self):

        sections_frame_width = self.sections_frame.width()

        num_of_day_frames = sections_frame_width // 100

        children_frames = [child for child in self.sections_frame.findChildren(QFrame) if child.parent() == self.sections_frame]
        num_children_frames = len(children_frames)

        if num_of_day_frames > num_children_frames:
            self.add_day_frames_to_sections_frame(num_of_day_frames, num_children_frames)

        elif num_of_day_frames < num_children_frames:
            self.remove_day_frames_to_sections_frame(num_of_day_frames)

        self.is_widget_shown = True

    def add_day_frames_to_sections_frame(self, num_of_day_frames, num_children_frames):
        for i in range(num_of_day_frames - num_children_frames):
            day_frame = DayFrame(self.left_most_day + timedelta(days=self.day_difference))
            day_frame.clicked.connect(self.update_selected_date_label)
            day_frame.clicked.connect(self.update_selected_day)
            self.sections_frame_h_layout.addWidget(day_frame)
            self.day_difference += 1

    def remove_day_frames_to_sections_frame(self, num_of_day_frames):

        self.sections_frame.setUpdatesEnabled(False)

        for i in reversed(range(num_of_day_frames, self.sections_frame_h_layout.count())):
            item = self.sections_frame_h_layout.itemAt(i)
            widget = item.widget()

            if isinstance(widget, QFrame):
                self.sections_frame_h_layout.removeWidget(widget)
                widget.setParent(None)
                widget.deleteLater()
                self.day_difference -= 1

        # Getting the date of the current rightmost day frame
        item = self.sections_frame_h_layout.itemAt(num_of_day_frames - 1)
        widget = item.widget()
        widget_date = widget.get_current_date()

        if self.selected_day > widget_date:
            self.update_selected_day(widget_date)
            self.update_selected_date_label(widget_date)

        self.sections_frame.setUpdatesEnabled(True)

    def set_external_stylesheet(self):
        with open("../resources/styles/reservation_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def set_icons(self):
        self.add_reservation_button.setIcon(QIcon("../resources/icons/reservation_page/add_icon.svg"))
        self.add_reservation_button.setIconSize(QSize(20, 20))

        self.left_button.setIcon(QIcon("../resources/icons/reservation_page/arrow_left_icon.svg"))
        self.left_button.setIconSize(QSize(20, 20))

        self.right_button.setIcon(QIcon("../resources/icons/reservation_page/arrow_right_icon.svg"))
        self.right_button.setIconSize(QSize(20, 20))

        self.reset_button.setIcon(QIcon("../resources/icons/reservation_page/refresh_icon.svg"))
        self.reset_button.setIconSize(QSize(20, 20))

    def load_fonts(self):
        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.reservation_and_bookings_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))
        self.selected_date_label.setFont(QFont("Inter", 18, QFont.Weight.Normal))

        self.view_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.add_reservation_button.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.reset_button.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))

    def showEvent(self, event):

        self.load_day_frames()

        super().showEvent(event)

    def resizeEvent(self, event):

        if self.is_widget_shown:
            QTimer.singleShot(0, self.load_day_frames)

        super().resizeEvent(event)
