
from .billing_page import BillingPage
from .booking_page import BookingPage
from .calendar_page import CalendarPage
from .dashboard_page import DashboardPage
from .guests_page import GuestsPage
from .reservation_page import ReservationPage
from .rooms_page import RoomsPage
from .services_page import ServicesPage
from .settings_page import SettingsPage

from .new_reservation_dialog import NewReservationDialog
from .guest_info_dialog import GuestInfoDialog

from .confirmation_dialog import ConfirmationDialog
from .feedback_dialog import FeedbackDialog

# When 'from views import *' is executed the classes in __all__ will be returned
# Only returns pages for now
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