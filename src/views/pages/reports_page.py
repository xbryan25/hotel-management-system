from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QColor

from ui import ReportsPageUI


class ReportsPage(QWidget, ReportsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

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
        self.apply_shadow(self.revenue_chart_frame)
        self.apply_shadow(self.reservation_status_chart_frame)
        self.apply_shadow(self.most_availed_services_chart_frame)
        self.apply_shadow(self.top_paying_guests_chart_frame)

    def set_external_stylesheet(self):
        with open("../resources/styles/reports_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.reports_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))
