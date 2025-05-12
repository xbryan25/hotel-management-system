from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox, QPushButton
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt, QSize

from datetime import datetime

from ui import ReservationInfoDialogUI
from views import ConfirmationDialog, FeedbackDialog


class ReservationInfoDialog(QDialog, ReservationInfoDialogUI):
    room_type_changed = pyqtSignal(str)
    room_changed = pyqtSignal(str)
    date_time_changed = pyqtSignal(str)
    spinbox_enabled = pyqtSignal()
    clicked_reservation = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)


        # self.update_current_date_and_time()
        #
        # self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()

        self.show_add_service_button(False)

    def show_add_service_button(self, state):
        self.add_service_button.setVisible(state)

    # def get_check_in_check_out_date_and_time(self):
    #     return {"check_in": self.check_in_date_time_edit.dateTime(),
    #             "check_out": self.check_out_date_time_edit.dateTime()}

    # def update_current_date_and_time(self):
    #     self.check_in_date_time_edit.setMinimumDateTime(QDateTime.currentDateTime().addDays(1))
    #     self.check_in_date_time_edit.setDateTime(QDateTime.currentDateTime().addDays(1))
    #
    #     self.check_out_date_time_edit.setMinimumDateTime(QDateTime.currentDateTime().addDays(2))
    #     self.check_out_date_time_edit.setDateTime(QDateTime.currentDateTime().addDays(2))

    # def update_check_out_date_time_edit_min_date(self):
    #     check_in_date_time_current_value = self.check_in_date_time_edit.dateTime()
    #
    #     self.check_out_date_time_edit.setMinimumDateTime(check_in_date_time_current_value.addDays(1))
    #     self.check_out_date_time_edit.setDateTime(check_in_date_time_current_value.addDays(1))
    #
    # def update_room_cost_value_label(self, room_cost):
    #     self.room_cost_value_label.setText(str(room_cost))
    #
    #     self.update_total_cost_value_label()
    #
    # def update_service_cost_value_label(self, total_service_cost):
    #
    #     if total_service_cost == 0:
    #         self.service_cost_value_label.setText("-")
    #     else:
    #         self.service_cost_value_label.setText(str(total_service_cost))
    #
    #     self.update_total_cost_value_label()
    #
    # def update_total_cost_value_label(self):
    #     room_cost = float(self.room_cost_value_label.text())
    #
    #     try:
    #         service_cost = float(self.service_cost_value_label.text())
    #     except ValueError:
    #         service_cost = 0
    #
    #     self.total_cost_value_label.setText(f"{room_cost + service_cost}")

    def create_service_frame(self, service):
        # TODO: Make into another file, I guess?

        frame = QFrame(parent=self.availed_services_scroll_area_widget_contents)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame.setObjectName(f"{service[1].replace(" ", "_")}_frame")
        # frame.setStyleSheet("background-color: blue;")
        # frame.setMinimumSize(QSize(16777215, 20))

        h_layout = QHBoxLayout(frame)
        h_layout.setObjectName(f"{service[1].replace(" ", "_")}_h_layout")

        service_name_label = QLabel(parent=frame)
        service_name_label.setObjectName(f"{service[1].replace(" ", "_")}_label")
        service_name_label.setText(service[1])
        service_name_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))
        h_layout.addWidget(service_name_label)

        spinbox = QSpinBox(parent=frame)
        spinbox.setObjectName(f"{service[1].replace(" ", "_")}_spinbox")
        spinbox.setFixedWidth(60)
        spinbox.setEnabled(False)
        spinbox.setMinimum(1)
        spinbox.setMaximum(99)
        spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        h_layout.addWidget(spinbox)

        h_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed,
                                         QSizePolicy.Policy.Minimum)
        h_layout.addItem(h_spacer)

        delete_push_button = QPushButton(parent=frame)
        delete_push_button.setMaximumSize(QSize(25, 25))
        delete_push_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        delete_push_button.setObjectName(f"{service[1].replace(" ", "_")}pushButton_3")
        delete_push_button.setEnabled(False)
        h_layout.addWidget(delete_push_button)

        frame.service_id = service[0]
        frame.spinbox = spinbox
        frame.service = service

        return frame

    def enable_spinbox(self, frame):
        pass

    def connect_signals_to_slots(self):

        pass

    def change_button_signals(self):
        pass


    def set_external_stylesheet(self):
        with open("../resources/styles/reservation_info_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.reservation_details_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.left_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.right_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.reservation_id_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.reservation_id_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.reservation_status_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.reservation_status_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.payment_status_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.payment_status_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.total_reservation_cost_label.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        self.total_reservation_cost_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.remaining_balance_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.remaining_balance_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.check_in_date_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.check_in_date_time_edit.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.check_out_date_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.check_out_date_time_edit.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.guest_id_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.guest_id_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.guest_name_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.guest_name_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_type_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_number_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_number_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.availed_services_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.add_service_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))


