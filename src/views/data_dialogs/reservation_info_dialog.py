from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox, QPushButton
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt, QSize

from datetime import datetime

from ui import ReservationInfoDialogUI
from views import ConfirmationDialog, FeedbackDialog


class ReservationInfoDialog(QDialog, ReservationInfoDialogUI):
    clicked_edit_button = pyqtSignal()
    clicked_cancel_edit_button = pyqtSignal()
    clicked_cancel_reservation_button = pyqtSignal()
    clicked_confirm_reservation_edit_button = pyqtSignal()
    clicked_proceed_button = pyqtSignal()

    spinbox_enabled = pyqtSignal()

    room_type_changed = pyqtSignal(str)
    room_changed = pyqtSignal(str)
    date_time_changed = pyqtSignal(str)

    def __init__(self, view_type):
        super().__init__()
        self.setupUi(self)

        self.dialog_state = 'not editable'
        self.view_type = view_type

        # self.update_current_date_and_time()

        self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()

    def load_proceed_button(self):
        self.left_button.setVisible(False)

    def hide_remaining_balance(self):
        self.remaining_balance_label.setVisible(False)
        self.remaining_balance_value_label.setVisible(False)

    def enable_all_editable_fields(self, service_frames, state):
        self.check_in_date_time_edit.setEnabled(state)
        self.check_out_date_time_edit.setEnabled(state)

        self.room_type_combobox.setEnabled(state)
        self.room_number_combobox.setEnabled(state)

        for service_frame in service_frames:
            service_frame.checkbox.setEnabled(state)

            if service_frame.checkbox.isChecked() and state:
                service_frame.spinbox.setEnabled(True)
            else:
                service_frame.spinbox.setEnabled(False)

        if not state:
            self.right_button.setEnabled(True)

    def get_check_in_check_out_date_and_time(self):
        return {"check_in": self.check_in_date_time_edit.dateTime(),
                "check_out": self.check_out_date_time_edit.dateTime()}

    def update_current_date_and_time(self, previous_check_in_date=None, previous_check_out_date=None, mode='different_room'):

        if mode == 'different_room':
            self.check_in_date_time_edit.setDateTime(QDateTime.currentDateTime().addDays(1))
            self.check_in_date_time_edit.setMinimumDateTime(QDateTime.currentDateTime().addDays(1))

            self.check_out_date_time_edit.setDateTime(QDateTime.currentDateTime().addDays(2))
            self.check_out_date_time_edit.setMinimumDateTime(QDateTime.currentDateTime().addDays(2))

        elif mode == 'same_room' and previous_check_in_date and previous_check_out_date:
            min_relaxed = QDateTime.fromString("2000-01-01T00:00:00", "yyyy-MM-ddTHH:mm:ss")
            self.check_in_date_time_edit.setMinimumDateTime(min_relaxed)
            self.check_out_date_time_edit.setMinimumDateTime(min_relaxed)

            self.check_in_date_time_edit.setDateTime(previous_check_in_date)
            self.check_out_date_time_edit.setDateTime(previous_check_out_date)

            min_check_in = QDateTime.currentDateTime().addDays(1)
            min_check_out = QDateTime.currentDateTime().addDays(2)

            if self.check_in_date_time_edit.dateTime() >= min_check_in:
                self.check_in_date_time_edit.setMinimumDateTime(min_check_in)
            else:
                self.check_in_date_time_edit.setMinimumDateTime(previous_check_in_date)

            if self.check_out_date_time_edit.dateTime() >= min_check_out:
                self.check_out_date_time_edit.setMinimumDateTime(min_check_out)
            else:
                self.check_out_date_time_edit.setMinimumDateTime(previous_check_out_date)

    def update_check_out_date_time_edit_min_date(self):
        check_in_date_time_current_value = self.check_in_date_time_edit.dateTime()

        self.check_out_date_time_edit.setMinimumDateTime(check_in_date_time_current_value.addDays(1))
        self.check_out_date_time_edit.setDateTime(check_in_date_time_current_value.addDays(1))

    def update_total_reservation_cost(self, total_reservation_cost):
        self.total_reservation_cost_value_label.setText(f"₱{int(total_reservation_cost)}")

    def create_service_frame(self, service, edit_state=False, service_type='not availed'):
        # TODO: Make into another file, I guess?

        frame = QFrame(parent=self.availed_services_scroll_area_widget_contents)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame.setObjectName(f"{service[1].replace(" ", "_")}_frame")

        h_layout = QHBoxLayout(frame)
        h_layout.setObjectName(f"{service[1].replace(" ", "_")}_h_layout")

        service_name_label = QLabel(parent=frame)
        service_name_label.setObjectName(f"{service[1].replace(" ", "_")}_label")
        service_name_label.setText(service[1])
        service_name_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))
        h_layout.addWidget(service_name_label)

        checkbox = QCheckBox(parent=frame)
        checkbox.setFixedWidth(30)
        checkbox.setEnabled(edit_state)
        checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        checkbox.setText("")
        checkbox.setObjectName(f"{service[1].replace(" ", "_")}_checkbox")
        h_layout.addWidget(checkbox)

        spinbox = QSpinBox(parent=frame)
        spinbox.setObjectName(f"{service[1].replace(" ", "_")}_spinbox")
        spinbox.setFixedWidth(60)
        spinbox.setEnabled(edit_state)
        spinbox.setMinimum(1)
        spinbox.setMaximum(99)
        spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        h_layout.addWidget(spinbox)

        h_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed,
                                         QSizePolicy.Policy.Minimum)
        h_layout.addItem(h_spacer)

        checkbox.checkStateChanged.connect(lambda _, f=frame: self.enable_spinbox(f))

        frame.service_id = service[0]
        frame.service_name = service[1]
        frame.checkbox = checkbox
        frame.spinbox = spinbox
        frame.service = service
        frame.service_type = service_type

        if service_type == 'availed':
            frame.service_rate = service[3]
            frame.is_spinbox_enabled = True
            frame.avail_id = service[4]

            spinbox.setValue(service[2])

            checkbox.blockSignals(True)
            checkbox.setCheckState(Qt.CheckState.Checked)
            checkbox.blockSignals(False)

        elif service_type == 'not availed':
            frame.service_rate = service[2]
            frame.is_spinbox_enabled = False
            frame.avail_id = None

        return frame

    def enable_spinbox(self, frame):
        if frame.spinbox.isEnabled():
            frame.spinbox.setEnabled(False)
            frame.is_spinbox_enabled = False
        else:
            frame.spinbox.setEnabled(True)
            frame.is_spinbox_enabled = True

        self.spinbox_enabled.emit()

    def clear_availed_services_layout(self):
        layout = self.availed_services_scroll_area_grid_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            elif item.spacerItem():
                layout.removeItem(item)

    def enable_edit_reservation_button(self, state):
        self.right_button.setEnabled(state)

    def connect_signals_to_slots(self):
        if self.view_type == 'current':
            self.check_in_date_time_edit.dateTimeChanged.connect(self.update_check_out_date_time_edit_min_date)

            self.check_in_date_time_edit.dateTimeChanged.connect(
                lambda: self.date_time_changed.emit(self.room_number_combobox.currentText()))

            self.check_out_date_time_edit.dateTimeChanged.connect(
                lambda: self.date_time_changed.emit(self.room_number_combobox.currentText()))

            self.room_type_combobox.currentTextChanged.connect(self.room_type_changed.emit)
            self.room_number_combobox.currentTextChanged.connect(self.room_changed.emit)

            self.change_button_signals()

        else:
            self.change_dialog_state_and_button_texts()
            self.right_button.clicked.connect(self.clicked_proceed_button.emit)

    def change_button_signals(self):
        self.remove_button_signals()

        if self.dialog_state == 'not editable':
            self.left_button.clicked.connect(self.clicked_cancel_reservation_button.emit)
            self.right_button.clicked.connect(self.clicked_edit_button.emit)
            self.right_button.clicked.connect(self.change_dialog_state_and_button_texts)
            self.right_button.clicked.connect(self.change_button_signals)

        elif self.dialog_state == 'editable':
            self.left_button.clicked.connect(self.clicked_cancel_edit_button.emit)
            self.left_button.clicked.connect(self.change_dialog_state_and_button_texts)
            self.left_button.clicked.connect(self.change_button_signals)
            self.right_button.clicked.connect(self.clicked_confirm_reservation_edit_button.emit)
            self.right_button.setEnabled(False)

    def change_dialog_state_and_button_texts(self):

        if self.view_type == 'current':
            if self.dialog_state == 'not editable':
                self.dialog_state = 'editable'

                self.left_button.setText("Cancel Edit")
                self.right_button.setText("Confirm Reservation Edit")
            else:
                self.dialog_state = 'not editable'

                self.left_button.setText("Cancel Reservation")
                self.right_button.setText("Edit Reservation")
        else:
            self.right_button.setText("Proceed")

    def get_reservation_inputs(self):
        reservation_inputs = {}

        reservation_inputs.update({"check_in_date": self.check_in_date_time_edit.dateTime().toPyDateTime()})
        reservation_inputs.update({"check_out_date": self.check_out_date_time_edit.dateTime().toPyDateTime()})
        reservation_inputs.update({"room_number": self.room_number_combobox.currentText()})
        reservation_inputs.update({"total_reservation_cost": self.total_reservation_cost_value_label.text()[1:]})

        return reservation_inputs

    @staticmethod
    def get_modified_availed_services_inputs(service_frames):
        availed_services_inputs = {}

        for frame in service_frames:

            if frame.service_type == 'availed':

                if frame.is_spinbox_enabled:
                    avail_status = 'active'
                else:
                    avail_status = 'cancelled'

                availed_services_inputs.update({frame.avail_id: {'quantity': frame.spinbox.value(),
                                                                 'avail_status': avail_status}})

        return availed_services_inputs

    @staticmethod
    def get_new_availed_services_inputs(service_frames):
        availed_services_inputs = {}

        for frame in service_frames:
            if frame.is_spinbox_enabled and frame.service_type == 'not availed':
                availed_services_inputs.update({frame.service_id: frame.spinbox.value()})

        return availed_services_inputs

    def remove_button_signals(self):
        self.left_button.disconnect()
        self.right_button.disconnect()

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
