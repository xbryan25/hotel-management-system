from datetime import datetime

from matplotlib.backends.backend_qtagg import FigureCanvasAgg, FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel


class ReportsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.revenue_canvas = None
        self.revenue_canvas_ax = None

        self.reservation_status_canvas = None
        self.reservation_status_canvas_ax = None

        self.most_availed_services_canvas = None
        self.most_availed_services_canvas_ax = None

        self.top_paying_guests_canvas = None
        self.top_paying_guests_canvas_ax = None

        self.prev_revenue_chart_choice = None

        self.load_all_charts()

    def connect_signals_to_slots(self):
        self.view.revenue_chart_combobox_changed.connect(self.update_revenue_chart)
        self.view.reservation_status_chart_combobox_changed.connect(self.update_reservation_status_chart)
        self.view.most_availed_services_chart_combobox_changed.connect(self.update_most_availed_services_chart)
        self.view.top_paying_guests_chart_combobox_changed.connect(self.update_top_paying_guests_chart)

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
        self.revenue_canvas_ax = fig.add_subplot()

        self.update_revenue_chart()

        self.view.revenue_chart_v_layout.addWidget(self.revenue_canvas)

    def load_reservation_status_chart(self):
        if self.reservation_status_canvas:
            self.view.reservation_status_chart_v_layout.removeWidget(self.reservation_status_canvas)
            self.reservation_status_canvas.setParent(None)
            self.reservation_status_canvas.deleteLater()
            self.reservation_status_canvas = None

        fig = Figure()
        self.reservation_status_canvas = FigureCanvasQTAgg(fig)
        self.reservation_status_canvas_ax = fig.add_subplot()

        self.update_reservation_status_chart()

        self.view.reservation_status_chart_v_layout.addWidget(self.reservation_status_canvas)

    def load_most_availed_services_chart(self):
        if self.most_availed_services_canvas:
            self.view.most_availed_services_chart_v_layout.removeWidget(self.most_availed_services_canvas)
            self.most_availed_services_canvas.setParent(None)
            self.most_availed_services_canvas.deleteLater()
            self.most_availed_services_canvas = None

        fig = Figure()
        self.most_availed_services_canvas = FigureCanvasQTAgg(fig)
        self.most_availed_services_canvas_ax = fig.add_subplot(111)

        self.update_most_availed_services_chart()

        fig.tight_layout()

        self.view.most_availed_services_chart_v_layout.addWidget(self.most_availed_services_canvas)

    def load_top_paying_guests_chart(self):
        if self.top_paying_guests_canvas:
            self.view.top_paying_guests_chart_v_layout.removeWidget(self.top_paying_guests_canvas)
            self.top_paying_guests_canvas.setParent(None)
            self.top_paying_guests_canvas.deleteLater()
            self.top_paying_guests_canvas = None

        fig = Figure()
        self.top_paying_guests_canvas = FigureCanvasQTAgg(fig)
        self.top_paying_guests_canvas_ax = fig.add_subplot(111)

        self.update_top_paying_guests_chart()

        fig.tight_layout()

        self.view.top_paying_guests_chart_v_layout.addWidget(self.top_paying_guests_canvas)

    def update_revenue_chart(self, view_type="Past 7 Days"):

        revenue_count = self.db_driver.paid_room_queries.get_count_of_revenue(view_type)

        x = []
        y = []

        for date, count in revenue_count:

            if view_type == "Past 4 Weeks":
                str_date = str(date)
                x.append(f"{str_date[:4]} W{str_date[4:]}")
            elif view_type == "Past 6 Months":
                x.append(f"{self.convert_num_to_month(date[5:])} {date[:4]}")
            else:
                x.append(date.strftime("%b %d"))

            y.append(count)

        self.revenue_canvas_ax.clear()  # Clear previous content if any
        self.revenue_canvas_ax.plot(x, y, marker='o', linestyle='-', color='black')
        self.revenue_canvas_ax.grid(True)

        self.revenue_canvas.draw()

    def update_most_availed_services_chart(self, view_type="Today"):
        most_availed_services_count = self.db_driver.availed_service_queries.get_count_of_most_availed_services(view_type)

        colors = ['#FFD700', '#32CD32', '#FF6347', '#A9A9A9', '#D9D9D9']
        labels = []
        values = []

        for service, count in most_availed_services_count:
            labels.append(service)
            values.append(count)

        self.most_availed_services_canvas_ax.clear()
        self.most_availed_services_canvas_ax.tick_params(axis='x', labelsize=7)

        self.most_availed_services_canvas_ax.bar(labels, values, color=colors)

        self.most_availed_services_canvas.draw()

    def update_top_paying_guests_chart(self, view_type="Today"):
        top_paying_guests_count = self.db_driver.guest_queries.get_top_paying_guests(view_type)

        colors = ['#FFD700', '#32CD32', '#FF6347', '#A9A9A9', '#D9D9D9']
        labels = []
        values = []

        for name, count in top_paying_guests_count:
            labels.append(self.truncate_text(name))
            values.append(count)

        self.top_paying_guests_canvas_ax.clear()
        self.top_paying_guests_canvas_ax.tick_params(axis='x', labelsize=7)

        self.top_paying_guests_canvas_ax.bar(labels, values, color=colors)
        self.top_paying_guests_canvas_ax.set_xticks(range(len(values)))

        self.top_paying_guests_canvas.draw()

    def update_reservation_status_chart(self, view_type="Today"):
        reservation_status_count = self.db_driver.reserved_room_queries.get_count_of_reservation_status(view_type)

        colors = ['#FFD700', '#32CD32', '#FF6347', '#A9A9A9']
        labels = []
        sizes = []
        total_count = 0

        for status, count in reservation_status_count:
            labels.append(status)
            total_count += count

        for _, count in reservation_status_count:
            sizes.append((count / total_count) * 100)

        self.reservation_status_canvas_ax.clear()
        self.reservation_status_canvas_ax.pie(sizes, labels=labels, colors=colors[:len(labels)],
                                              autopct=lambda p: self.both_numbers_and_percentages(p, total_count),
                                              startangle=90)
        self.reservation_status_canvas_ax.axis('equal')
        self.reservation_status_canvas.draw()

    @staticmethod
    def both_numbers_and_percentages(pct, total_count):
        absolute = int(round(pct * total_count / 100.0))
        return f"{absolute} ({pct:.1f}%)"

    @staticmethod
    def truncate_text(text, max_length=10):
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    @staticmethod
    def convert_num_to_month(num):
        months = {
            "01": "January",
            "02": "Feb",
            "03": "Mar",
            "04": "Apr",
            "05": "May",
            "06": "Jun",
            "07": "Jul",
            "08": "Aug",
            "09": "Sep",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec",
        }

        return months[num]
