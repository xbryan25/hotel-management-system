
from .billing_page import BillingPage
from .booking_page import BookingPage
from .calendar_page import CalendarPage
from .dashboard_page import DashboardPage
from .guests_page import GuestsPage
from .reservation_page import ReservationPage
from .rooms_page import RoomsPage
from .services_page import ServicesPage
from .settings_page import SettingsPage

# When 'from views import *' is executed the classes in __all__ will be returned
__all__ = [
    "BillingPage",
    "BookingPage",
    "CalendarPage",
    "DashboardPage",
    "GuestsPage",
    "ReservationPage",
    "RoomsPage",
    "ServicesPage",
    "SettingsPage"
]