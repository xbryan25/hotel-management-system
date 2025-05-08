from PyQt6.QtCore import QTime, QTimer
from PyQt6.QtWidgets import QWidget, QFrame

from ui import ReservationPageUI

from views.custom_widgets import DayFrame

from datetime import date, timedelta


class ReservationPage(QWidget, ReservationPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.is_widget_shown = False

        self.day_difference = 0

    def load_day_frames(self):

        sections_frame_width = self.sections_frame.width()

        num_of_day_frames = sections_frame_width // 80

        children_frames = [child for child in self.sections_frame.findChildren(QFrame) if child.parent() == self.sections_frame]
        num_children_frames = len(children_frames)

        if num_of_day_frames > num_children_frames:
            self.add_day_frames_to_sections_frame(num_of_day_frames, num_children_frames)

        elif num_of_day_frames < num_children_frames:
            self.remove_day_frames_to_sections_frame(num_of_day_frames)

        self.is_widget_shown = True

    def add_day_frames_to_sections_frame(self, num_of_day_frames, num_children_frames):
        for i in range(num_of_day_frames - num_children_frames):
            self.sections_frame_h_layout.addWidget(DayFrame(date.today() + timedelta(days=self.day_difference)))
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

        self.sections_frame.setUpdatesEnabled(True)


    def showEvent(self, event):

        self.load_day_frames()

        super().showEvent(event)

    def resizeEvent(self, event):

        if self.is_widget_shown:
            QTimer.singleShot(0, self.load_day_frames)

        super().resizeEvent(event)
