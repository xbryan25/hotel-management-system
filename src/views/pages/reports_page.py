from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import pyqtSignal, QTimer

from ui import ReportsPageUI


class ReportsPage(QWidget, ReportsPageUI):
    revenue_chart_combobox_changed = pyqtSignal(str)
    reservation_status_chart_combobox_changed = pyqtSignal(str)
    most_availed_services_chart_combobox_changed = pyqtSignal(str)
    top_paying_guests_chart_combobox_changed = pyqtSignal(str)
    window_resized = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.connect_signals_to_slots()

        self.set_external_stylesheet()
        self.load_fonts()

        self.apply_shadow_to_frames()

        self.old_width = self.width()
        self.old_height = self.height()

        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.window_resized.emit)

    @staticmethod
    def apply_shadow(widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)

    def apply_shadow_to_frames(self):
        self.apply_shadow(self.revenue_chart_frame)
        self.apply_shadow(self.reservation_status_chart_frame)
        self.apply_shadow(self.most_availed_services_chart_frame)
        self.apply_shadow(self.top_paying_guests_chart_frame)

    def connect_signals_to_slots(self):
        self.revenue_chart_combobox.currentTextChanged.connect(self.revenue_chart_combobox_changed.emit)

        self.reservation_status_chart_combobox.currentTextChanged.connect(self.reservation_status_chart_combobox_changed.emit)

        self.most_availed_services_chart_combobox.currentTextChanged.connect(self.most_availed_services_chart_combobox_changed.emit)

        self.top_paying_guests_chart_combobox.currentTextChanged.connect(self.top_paying_guests_chart_combobox_changed.emit)

    def set_external_stylesheet(self):
        with open("../resources/styles/reports_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.reports_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.revenue_chart_text_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.revenue_chart_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.reservation_status_chart_text_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.reservation_status_chart_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.most_availed_services_chart_text_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.most_availed_services_chart_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.top_paying_guests_chart_text_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.top_paying_guests_chart_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.resize_timer.start(200)
