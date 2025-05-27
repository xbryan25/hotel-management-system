from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox
from PyQt6.QtGui import QCursor, QFont, QRegularExpressionValidator, QIcon
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt, QRegularExpression, QSize

from datetime import datetime

from ui import NewReservationDialogUI
from views import ConfirmationDialog, FeedbackDialog, IssuesDialog
from utils import InputValidators


class NewReservationDialog(QDialog, NewReservationDialogUI):
    room_type_changed = pyqtSignal(str)
    room_changed = pyqtSignal(str)
    selected_reservation_duration = pyqtSignal(datetime, datetime)
    date_time_changed = pyqtSignal(str)
    spinbox_enabled = pyqtSignal()
    clicked_reservation = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_page = 1

        self.update_current_date_and_time()

        self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()
        self.set_icons()

        self.set_phone_number_lineedit_validator()
        self.set_lineedits_max_length()

    def set_guest_count_spinbox_max_value(self, max_value):
        self.guest_count_spinbox.setMaximum(max_value)

    def set_phone_number_lineedit_validator(self):

        regex = QRegularExpression("^[0-9]*$")
        validator = QRegularExpressionValidator(regex)

        self.phone_number_lineedit.setValidator(validator)
        self.phone_number_lineedit.setMaxLength(11)

    def set_lineedits_max_length(self):
        self.first_name_lineedit.setMaxLength(127)
        self.last_name_lineedit.setMaxLength(127)

        self.home_address_lineedit.setMaxLength(255)
        self.email_address_lineedit.setMaxLength(255)
        self.government_id_number_lineedit.setMaxLength(255)

    def get_check_in_check_out_date_and_time(self):
        return {"check_in": self.check_in_date_time_edit.dateTime(),
                "check_out": self.check_out_date_time_edit.dateTime()}

    def update_current_date_and_time(self):
        self.check_in_date_time_edit.setMinimumDateTime(QDateTime.currentDateTime().addDays(1))
        self.check_in_date_time_edit.setDateTime(QDateTime.currentDateTime().addDays(1))

        self.check_out_date_time_edit.setMinimumDateTime(QDateTime.currentDateTime().addDays(2))
        self.check_out_date_time_edit.setDateTime(QDateTime.currentDateTime().addDays(2))

    def update_check_out_date_time_edit_min_date(self):
        check_in_date_time_current_value = self.check_in_date_time_edit.dateTime()

        self.check_out_date_time_edit.setMinimumDateTime(check_in_date_time_current_value.addDays(1))
        self.check_out_date_time_edit.setDateTime(check_in_date_time_current_value.addDays(1))

    def update_room_cost_value_label(self, room_cost):
        self.room_cost_value_label.setText(str(room_cost))

        self.update_total_cost_value_label()

    def update_service_cost_value_label(self, total_service_cost):

        if total_service_cost == 0:
            self.service_cost_value_label.setText("-")
        else:
            self.service_cost_value_label.setText(str(total_service_cost))

        self.update_total_cost_value_label()

    def update_total_cost_value_label(self):
        room_cost = float(self.room_cost_value_label.text())

        try:
            service_cost = float(self.service_cost_value_label.text())
        except ValueError:
            service_cost = 0

        self.total_cost_value_label.setText(f"{room_cost + service_cost}")

    def create_service_frame(self, service):

        frame = QFrame(parent=self.services_scroll_area_contents)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame_object_name = f"{service[1].replace(" ", "_")}_frame"
        frame.setObjectName(frame_object_name)
        frame.setStyleSheet(f"#{frame_object_name}{{background-color: transparent; border: 1px solid #d9d9d9;}}")

        h_layout = QHBoxLayout(frame)
        h_layout.setObjectName(f"{service[1].replace(" ", "_")}_h_layout")

        service_name_label = QLabel(parent=frame)
        service_name_label.setObjectName(f"{service[1].replace(" ", "_")}_label")
        service_name_label.setText(service[1])
        service_name_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        h_layout.addWidget(service_name_label)

        checkbox = QCheckBox(parent=frame)
        checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        checkbox.setText("")
        checkbox.setObjectName(f"{service[1].replace(" ", "_")}_checkbox")
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #888888;
                background-color: #f0f0f0;
            }
            
            QCheckBox::indicator:checked {
                image: url(../resources/icons/check.svg);
            }
            
            QCheckBox::indicator:checked:hover, QCheckBox::indicator:unchecked:hover {
                background-color: #e0e0e0;
            }
        """)
        h_layout.addWidget(checkbox)

        spinbox = QSpinBox(parent=frame)
        spinbox.setObjectName(f"{service[1].replace(" ", "_")}_spinbox")
        spinbox.setEnabled(False)
        spinbox.setMinimum(1)
        spinbox.setMaximum(99)
        spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #d9d9d9; 
                color: #000000;
            }
            QSpinBox:disabled {
                background-color: #f0f0f0;  
                color: #888888;             
            }
        """)
        h_layout.addWidget(spinbox)

        checkbox.checkStateChanged.connect(lambda _, f=frame: self.enable_spinbox(f))

        frame.service_id = service[0]
        frame.spinbox = spinbox
        frame.service = service
        frame.is_spinbox_enabled = False

        return frame

    def enable_spinbox(self, frame):
        frame_object_name = frame.objectName()

        if frame.spinbox.isEnabled():
            frame.spinbox.setEnabled(False)
            frame.is_spinbox_enabled = False
            frame.setStyleSheet(f"#{frame_object_name}{{background-color: transparent; border: 1px solid #d9d9d9;}}")
        else:
            frame.spinbox.setEnabled(True)
            frame.is_spinbox_enabled = True
            frame.setStyleSheet(f"#{frame_object_name}{{background-color: #c0c0c0; border: 1px solid #d9d9d9;}}")

        self.spinbox_enabled.emit()

    def connect_signals_to_slots(self):

        self.check_in_date_time_edit.dateTimeChanged.connect(self.update_check_out_date_time_edit_min_date)
        self.check_in_date_time_edit.dateTimeChanged.connect(lambda: self.date_time_changed.emit(self.rooms_combobox.currentText()))

        self.check_out_date_time_edit.dateTimeChanged.connect(lambda: self.date_time_changed.emit(self.rooms_combobox.currentText()))

        self.room_type_filter_combobox.currentTextChanged.connect(self.room_type_changed.emit)
        self.rooms_combobox.currentTextChanged.connect(self.room_changed.emit)

        self.change_button_signals()

    def change_button_signals(self):
        self.remove_button_signals()

        if self.current_page == 1:
            self.left_button.clicked.connect(self.close)
            self.right_button.clicked.connect(self.emit_selected_reservation_duration)

        elif self.current_page == 2:
            self.left_button.clicked.connect(lambda: self.page_change("left_button"))
            self.right_button.clicked.connect(self.validate_form_completion)

        elif self.current_page == 3:
            self.left_button.clicked.connect(lambda: self.page_change("left_button"))
            self.right_button.clicked.connect(self.confirm_reservation)

        self.left_button.clicked.connect(self.change_button_signals)
        self.right_button.clicked.connect(self.change_button_signals)

    def emit_selected_reservation_duration(self):
        self.selected_reservation_duration.emit(self.check_in_date_time_edit.dateTime().toPyDateTime(),
                                                self.check_out_date_time_edit.dateTime().toPyDateTime())

    def remove_button_signals(self):
        self.left_button.disconnect()
        self.right_button.disconnect()

    def get_guest_inputs(self):
        guest_inputs = {}

        guest_inputs.update({"name": f"{self.first_name_lineedit.text()} {self.last_name_lineedit.text()}"})
        guest_inputs.update({"gender": self.gender_combobox.currentText()})
        guest_inputs.update({"birth_date": self.birth_date_dateedit.date().toPyDate()})
        guest_inputs.update({"home_address": self.home_address_lineedit.text()})
        guest_inputs.update({"email_address": self.email_address_lineedit.text()})
        guest_inputs.update({"government_id": self.government_id_number_lineedit.text()})
        guest_inputs.update({"phone_number": self.phone_number_lineedit.text()})

        return guest_inputs

    def get_reservation_inputs(self):
        reservation_inputs = {}

        reservation_inputs.update({"reservation_date": datetime.now()})
        reservation_inputs.update({"last_modified": datetime.now()})
        reservation_inputs.update({"payment_status": "not paid"})
        reservation_inputs.update({"check_in_date": self.check_in_date_time_edit.dateTime().toPyDateTime()})
        reservation_inputs.update({"check_out_date": self.check_out_date_time_edit.dateTime().toPyDateTime()})
        reservation_inputs.update({"room_number": self.rooms_combobox.currentText()})
        reservation_inputs.update({"total_reservation_cost": self.total_cost_value_label.text()})
        reservation_inputs.update({"reservation_status": "pending"})
        reservation_inputs.update({"guest_count": int(self.guest_count_spinbox.value())})

        return reservation_inputs

    @staticmethod
    def get_availed_services_inputs(service_frames):
        availed_services_inputs = {}

        for frame in service_frames:
            if frame.is_spinbox_enabled:
                availed_services_inputs.update({frame.service_id: frame.spinbox.value()})

        return availed_services_inputs

    def validate_form_completion(self):

        guest_inputs = {"First name": self.first_name_lineedit.text(),
                        "Last name": self.last_name_lineedit.text(),
                        "Home address": self.home_address_lineedit.text(),
                        "Email address": self.email_address_lineedit.text(),
                        "Phone number": self.phone_number_lineedit.text(),
                        "Government ID number": self.government_id_number_lineedit.text()}

        issues = ""

        for guest_input in guest_inputs:

            if guest_inputs[guest_input] and guest_input == "Email address" and not InputValidators.is_valid_email(guest_inputs[guest_input]):
                issues += f"- {guest_input} is invalid.\n"

            elif guest_inputs[guest_input] and guest_input == "Phone number" and not InputValidators.is_valid_phone_number(guest_inputs[guest_input]):
                issues += f"- {guest_input} is invalid.\n        Format: 09XXXXXXXXX\n"

            elif not guest_inputs[guest_input]:
                issues += f"- {guest_input} is empty.\n"

        if not issues:
            self.page_change("right_button")
        else:
            self.issues_dialog = IssuesDialog("Issues found:", issues)
            self.issues_dialog.exec()

    def confirm_reservation(self):
        header_message = "Are you sure you want to make this reservation?"
        subheader_message = "Double check all input fields before proceeding."
        self.confirmation_dialog = ConfirmationDialog(header_message, subheader_message)

        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_choice():
            self.clicked_reservation.emit()

    def page_change(self, button_type):
        if self.current_page < 3 and button_type == "right_button":
            self.current_page += 1
        elif self.current_page > 1 and button_type == "left_button":
            self.current_page -= 1

        if self.current_page == 1:
            self.left_button.setText("Cancel")
        elif self.current_page == 2:
            self.left_button.setText("Back")
            self.right_button.setText("Next")
        else:
            self.right_button.setText("Reserve")

        self.contents_stacked_widget.setCurrentIndex(self.current_page - 1)

    def set_icons(self):
        self.room_reservations_button.setIcon(QIcon("../resources/icons/info_icon.svg"))
        self.room_reservations_button.setIconSize(QSize(30, 30))

    def set_external_stylesheet(self):
        with open("../resources/styles/new_reservation_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.add_new_reservation_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.left_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.right_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.cost_summary_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        self.room_cost_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))
        self.service_cost_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))
        self.total_cost_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.room_cost_value_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))
        self.service_cost_value_label.setFont(QFont("Inter", 14, QFont.Weight.Normal))
        self.total_cost_value_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))

        self.reservation_details_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        self.room_reservations_button.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.check_in_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.check_out_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_type_filter_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.rooms_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.guest_count_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.check_in_date_time_edit.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.check_out_date_time_edit.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.room_type_filter_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.rooms_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.guest_count_spinbox.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.primary_booker_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        self.first_name_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.last_name_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.gender_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.birth_date_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.home_address_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.email_address_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.phone_number_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.government_id_number_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.first_name_lineedit.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.last_name_lineedit.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.gender_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.birth_date_dateedit.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.home_address_lineedit.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.email_address_lineedit.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.phone_number_lineedit.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.government_id_number_lineedit.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.additional_service_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
