from datetime import datetime

from matplotlib.backends.backend_qtagg import FigureCanvasAgg, FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel


class ReportsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.revenue_canvas = None
        self.reservation_status_canvas = None
        self.most_availed_services_canvas = None
        self.top_paying_guests_canvas = None

        self.load_all_charts()

    def connect_signals_to_slots(self):
        self.view.revenue_chart_combobox_changed.connect(self.update_revenue_chart)
        self.view.reservation_status_chart_combobox_changed.connect(lambda text: print(text))
        self.view.most_availed_services_chart_combobox_changed.connect(lambda text: print(text))
        self.view.top_paying_guests_chart_combobox_changed.connect(lambda text: print(text))

        # self.view.window_resized.connect(self.load_all_charts)

    def load_all_charts(self):
        self.load_revenue_chart()
        self.load_reservation_status_chart()
        self.load_most_availed_services_chart()
        self.load_top_paying_guests_chart()

    def load_revenue_chart(self, view_type="Past 7 Days"):

        if self.revenue_canvas:
            self.view.revenue_chart_v_layout.removeWidget(self.revenue_canvas)
            self.revenue_canvas.setParent(None)
            self.revenue_canvas.deleteLater()
            self.revenue_canvas = None

        fig = Figure()
        self.revenue_canvas = FigureCanvasQTAgg(fig)
        ax = fig.add_subplot()

        x = [1, 2, 3, 4, 5]
        y = [9, 3, 5, 1, 4]
        ax.plot(x, y)

        self.view.revenue_chart_v_layout.addWidget(self.revenue_canvas)

    def load_reservation_status_chart(self, view_type="Past 7 Days"):
        if self.reservation_status_canvas:
            self.view.reservation_status_chart_v_layout.removeWidget(self.reservation_status_canvas)
            self.reservation_status_canvas.setParent(None)
            self.reservation_status_canvas.deleteLater()
            self.reservation_status_canvas = None

        fig = Figure()
        self.reservation_status_canvas = FigureCanvasQTAgg(fig)
        ax = fig.add_subplot()

        x = [1, 2, 3, 4, 5]
        y = [9, 3, 5, 1, 4]
        ax.plot(x, y)

        self.view.reservation_status_chart_v_layout.addWidget(self.reservation_status_canvas)

    def load_most_availed_services_chart(self, view_type="Past 7 Days"):
        if self.most_availed_services_canvas:
            self.view.most_availed_services_chart_v_layout.removeWidget(self.most_availed_services_canvas)
            self.most_availed_services_canvas.setParent(None)
            self.most_availed_services_canvas.deleteLater()
            self.most_availed_services_canvas = None

        fig = Figure()
        self.most_availed_services_canvas = FigureCanvasQTAgg(fig)
        ax = fig.add_subplot()

        x = [1, 2, 3, 4, 5]
        y = [9, 3, 5, 1, 4]
        ax.plot(x, y)

        self.view.most_availed_services_chart_v_layout.addWidget(self.most_availed_services_canvas)

    def load_top_paying_guests_chart(self, view_type="Past 7 Days"):
        if self.top_paying_guests_canvas:
            self.view.top_paying_guests_chart_v_layout.removeWidget(self.top_paying_guests_canvas)
            self.top_paying_guests_canvas.setParent(None)
            self.top_paying_guests_canvas.deleteLater()
            self.top_paying_guests_canvas = None

        fig = Figure()
        self.top_paying_guests_canvas = FigureCanvasQTAgg(fig)
        ax = fig.add_subplot()

        x = [1, 2, 3, 4, 5]
        y = [9, 3, 5, 1, 4]
        ax.plot(x, y)

        self.view.top_paying_guests_chart_v_layout.addWidget(self.top_paying_guests_canvas)

    def update_data_of_charts(self):
        self.update_revenue_chart()

    def update_revenue_chart(self, view_type="Past 7 Days"):
        print(view_type)