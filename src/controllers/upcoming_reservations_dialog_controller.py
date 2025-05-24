from PyQt6.QtWidgets import QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class UpcomingReservationsDialogController:
    def __init__(self, dialog, db_driver, room_number):
        self.view = dialog
        self.db_driver = db_driver
        self.room_number = room_number

        self.setup_reservations_label()

        self.load_reservation_dates()

    def setup_reservations_label(self):
        self.view.setup_reservations_label(self.room_number)

    def load_reservation_dates(self):
        room_id = self.db_driver.room_queries.get_room_id_from_room_number(self.room_number)

        reservation_dates = self.db_driver.reserved_room_queries.get_all_check_in_and_check_out_of_room(room_id)

        for i in range(len(reservation_dates)):
            date_label = QLabel(parent=self.view.reservation_dates_scroll_area_contents)

            date_label.setText(f"""• {reservation_dates[i][0].strftime('%b %d, %Y %I:%M %p')} - {reservation_dates[i][1].strftime('%b %d, %Y %I:%M %p')}""")
            date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            date_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))

            self.view.reservation_dates_scroll_area_grid_layout.addWidget(date_label)

        v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.view.reservation_dates_scroll_area_grid_layout.addItem(v_spacer)
