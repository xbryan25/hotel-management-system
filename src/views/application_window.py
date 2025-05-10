from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
from PyQt6.QtCore import Qt, QSize

from ui import ApplicationWindowUI
from utils import SidebarCursorChanger
from db import DatabaseDriver
from controllers import *
from views import *


class ApplicationWindow(QMainWindow, ApplicationWindowUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.db_driver = DatabaseDriver()

        self.collapsed_sidebar_frame.setVisible(False)

        self.initialize_sidebar()
        self.add_icon_to_toggle_sidebar_button()

        self.set_external_stylesheet()
        self.load_fonts()
        self.apply_fonts()

        self.setup_toggle_sidebar_button()
        self.add_signals_to_sidebar_items()

        self.load_pages()
        self.setup_controllers()

    def show_collapsed_sidebar_frame(self):
        self.collapsed_sidebar_frame.setVisible(True)
        self.expanded_sidebar_frame.setVisible(False)

    def show_expanded_sidebar_frame(self):
        self.collapsed_sidebar_frame.setVisible(False)
        self.expanded_sidebar_frame.setVisible(True)

    def add_signals_to_sidebar_items(self):
        # Connects the index of the list widget to the index of the stacked widget
        self.expanded_buttons_list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.collapsed_buttons_list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # Connects the expanded buttons list widget to the collapsed buttons list widget and vice versa
        self.expanded_buttons_list_widget.currentRowChanged.connect(self.collapsed_buttons_list_widget.setCurrentRow)
        self.collapsed_buttons_list_widget.currentRowChanged.connect(self.expanded_buttons_list_widget.setCurrentRow)

    def setup_toggle_sidebar_button(self):
        self.show_icons_only_button.clicked.connect(self.show_collapsed_sidebar_frame)
        self.show_icons_and_text_button.clicked.connect(self.show_expanded_sidebar_frame)

    def add_icon_to_toggle_sidebar_button(self):
        self.show_icons_only_button.setIcon(QIcon("../resources/icons/sidebar/expand_sidebar_icon.svg"))
        self.show_icons_and_text_button.setIcon(QIcon("../resources/icons/sidebar/collapse_sidebar_icon.svg"))

        self.show_icons_only_button.setIconSize(QSize(28, 28))
        self.show_icons_and_text_button.setIconSize(QSize(28, 28))

    def initialize_sidebar(self):
        self.sidebar_list = [{"name": "Dashboard", "icon": "../resources/icons/sidebar/dashboard_icon.svg"},
                             {"name": "Rooms", "icon": "../resources/icons/sidebar/rooms_icon.svg"},
                             {"name": "Calendar", "icon": "../resources/icons/sidebar/calendar_icon.svg"},
                             {"name": "Reservation", "icon": "../resources/icons/sidebar/reservation_icon.svg"},
                             {"name": "Booking", "icon": "../resources/icons/sidebar/booking_icon.svg"},
                             {"name": "Guests", "icon": "../resources/icons/sidebar/guests_icon.svg"},
                             {"name": "Billing", "icon": "../resources/icons/sidebar/billing_icon.svg"},
                             {"name": "Services", "icon": "../resources/icons/sidebar/services_icon.svg"},
                             {"name": "Settings", "icon": "../resources/icons/sidebar/settings_icon.svg"}]


        self.expanded_buttons_list_widget.clear()
        self.collapsed_buttons_list_widget.clear()

        self.expanded_buttons_list_widget.setIconSize(QSize(28, 28))
        self.collapsed_buttons_list_widget.setIconSize(QSize(28, 28))

        for sidebar_item in self.sidebar_list:

            # For collapsed buttons list widget (icons only)
            item_collapsed = QListWidgetItem()
            item_collapsed.setIcon(QIcon(sidebar_item.get("icon")))
            # item_collapsed.setSizeHint(QSize(50, 50))

            self.collapsed_buttons_list_widget.addItem(item_collapsed)
            self.collapsed_buttons_list_widget.setCurrentRow(0)

            # For expanded buttons list widget (icons and text)
            item_expanded = QListWidgetItem()
            item_expanded.setIcon(QIcon(sidebar_item.get("icon")))
            item_expanded.setText(sidebar_item.get("name"))
            # item_expanded.setSizeHint(QSize(50, 50))

            self.expanded_buttons_list_widget.addItem(item_expanded)
            self.expanded_buttons_list_widget.setCurrentRow(0)

        # Attach event filter (sidebar cursor changer)
        # Installed on viewport instead of the list widget itself

        cursor_filter_collapsed = SidebarCursorChanger(self.collapsed_buttons_list_widget)
        self.collapsed_buttons_list_widget.viewport().installEventFilter(cursor_filter_collapsed)

        # setMouseTracking of the viewport is also set to True
        self.collapsed_buttons_list_widget.viewport().setMouseTracking(True)

        cursor_filter_expanded = SidebarCursorChanger(self.expanded_buttons_list_widget)
        self.expanded_buttons_list_widget.viewport().installEventFilter(cursor_filter_expanded)
        self.expanded_buttons_list_widget.viewport().setMouseTracking(True)

        self.collapsed_buttons_list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.expanded_buttons_list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def load_pages(self):
        self.billing_page = BillingPage()
        self.booking_page = BookingPage()
        self.calendar_page = CalendarPage()
        self.dashboard_page = DashboardPage()
        self.guests_page = GuestsPage()
        self.reservation_page = ReservationPage()
        self.rooms_page = RoomsPage()
        self.services_page = ServicesPage()
        self.settings_page = SettingsPage()

        # Loaded according to index of sidebar
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.rooms_page)
        self.stacked_widget.addWidget(self.calendar_page)
        self.stacked_widget.addWidget(self.reservation_page)
        self.stacked_widget.addWidget(self.booking_page)
        self.stacked_widget.addWidget(self.guests_page)
        self.stacked_widget.addWidget(self.billing_page)
        self.stacked_widget.addWidget(self.services_page)
        self.stacked_widget.addWidget(self.settings_page)

        self.stacked_widget.setCurrentWidget(self.dashboard_page)

    def set_external_stylesheet(self):
        with open("../resources/styles/sidebar.qss", "r") as file:
            self.sidebar_frame.setStyleSheet(file.read())

    def load_fonts(self):
        # Load fonts, they can be used in any part of the application
        QFontDatabase.addApplicationFont("../resources/fonts/Inter-Light.otf")
        QFontDatabase.addApplicationFont("../resources/fonts/Inter-Medium.otf")
        QFontDatabase.addApplicationFont("../resources/fonts/Inter-SemiBold.otf")
        QFontDatabase.addApplicationFont("../resources/fonts/Inter-Bold.otf")
        QFontDatabase.addApplicationFont("../resources/fonts/Inter-ExtraBold.otf")
        QFontDatabase.addApplicationFont("../resources/fonts/Inter-Black.otf")
        QFontDatabase.addApplicationFont("../resources/fonts/Inter-Regular.otf")

        QFontDatabase.addApplicationFont("../resources/fonts/ABeeZee-Regular.ttf")

    def apply_fonts(self):
        self.title_label.setFont(QFont("ABeeZee", 28, QFont.Weight.Light))
        self.expanded_buttons_list_widget.setFont(QFont("Inter", 14, QFont.Weight.Medium))

    def setup_controllers(self):
        self.dashboard_controller = DashboardController(self.dashboard_page, self.db_driver)
        self.rooms_page_controller = RoomsPageController(self.rooms_page, self.db_driver)
        self.guests_page_controller = GuestsPageController(self.guests_page, self.db_driver)
        self.services_page_controller = ServicesPageController(self.services_page, self.db_driver)
        self.reservations_page_controller = ReservationsPageController(self.reservation_page, self.db_driver)
        self.bookings_page_controller = BookingsPageController(self.booking_page, self.db_driver)

    def closeEvent(self, event):
        self.db_driver.close_connection()
