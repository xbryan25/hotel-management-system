from PyQt6.QtCore import QTime, QDateTime, QTimer

from models import RecentStaysModel, ReservationModel, RoomsModel
from views import NewReservationDialog
from views.message_dialogs import FeedbackDialog

from controllers.new_reservation_dialog_controller import NewReservationDialogController


class DashboardController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.load_data()
        self.view.set_table_views_column_widths()

        # Set up timer to update every 60,000 ms (60 seconds)
        self.update_date_and_time_timer = QTimer(self.view)
        self.update_date_and_time_timer.timeout.connect(self.update_date_and_time)

        self.update_date_and_time()
        self.sync_timer_to_next_minute()

    def connect_signals_to_slots(self):
        self.view.clicked_new_reservation_button.connect(self.open_new_reservation_dialog)

        self.view.changed_room_status.connect(self.update_rooms_view)

    def open_new_reservation_dialog(self):
        if self.db_driver.room_queries.has_available_room():
            self.new_reservation_dialog = NewReservationDialog()
            self.new_reservation_dialog_controller = NewReservationDialogController(self.new_reservation_dialog, self.db_driver)

            self.new_reservation_dialog.exec()

        else:
            self.no_room_dialog = FeedbackDialog(header_message="No more available rooms.",
                                                 subheader_message="Please try again later.")
            self.no_room_dialog.exec()

    def update_date_and_time(self):

        current_time = QDateTime.currentDateTime().toString("hh:mm A")
        current_day = QDateTime.currentDateTime().toString("ddd, MMM d")

        self.view.current_time_label.setText(f"{current_time}")
        self.view.current_day_label.setText(f"{current_day}")

    def sync_timer_to_next_minute(self):
        time_now = QTime.currentTime()

        # seconds until next minute - milliseconds until next second
        msecs_to_next_minute = (60 - time_now.second()) * 1000 - time_now.msec()

        QTimer.singleShot(msecs_to_next_minute, self.start_minute_timer)
        QTimer.singleShot(msecs_to_next_minute, self.update_date_and_time)

    def start_minute_timer(self):
        self.update_date_and_time_timer.start(60000)

    def load_data(self):
        self.set_models()
        self.load_data_in_labels()

    def set_models(self):
        recent_check_in_initial_data = self.db_driver.booked_room_queries.get_all_booked_room_today("check_in")
        recent_check_out_initial_data = self.db_driver.booked_room_queries.get_all_booked_room_today("check_out")
        reservations_initial_data = self.db_driver.reserved_room_queries.get_all_reservations()
        rooms_initial_data = self.db_driver.room_queries.get_all_rooms()

        self.recent_check_in_table_model = RecentStaysModel(recent_check_in_initial_data)
        self.recent_check_out_table_model = RecentStaysModel(recent_check_out_initial_data)
        self.reservation_table_model = ReservationModel(reservations_initial_data, "dashboard_view")
        self.rooms_model = RoomsModel(rooms_initial_data)

        self.view.recent_check_in_frame_table_view.setModel(self.recent_check_in_table_model)
        self.view.recent_check_out_frame_table_view.setModel(self.recent_check_out_table_model)
        self.view.reservation_list_frame_table_view.setModel(self.reservation_table_model)
        self.view.rooms_frame_table_view.setModel(self.rooms_model)

    def load_data_in_labels(self):
        self.view.today_check_in_frame_num_label.setText(
            str(self.db_driver.booked_room_queries.get_count_all_booked_room_today('check_in')))

        self.view.today_check_out_frame_num_label.setText(
            str(self.db_driver.booked_room_queries.get_count_all_booked_room_today('check_out')))

        self.view.available_rooms_frame_num_label.setText(
            str(self.db_driver.room_queries.get_room_count('Available')))

        self.view.reserved_rooms_frame_num_label.setText(
            str(self.db_driver.room_queries.get_room_count('Reserved')))

        self.view.booked_rooms_frame_num_label.setText(
            str(self.db_driver.room_queries.get_room_count('Occupied')))

    def update_rooms_view(self, room_status):

        rooms_initial_data = self.db_driver.room_queries.get_all_rooms(room_status)
        self.rooms_model.update_data(rooms_initial_data)
