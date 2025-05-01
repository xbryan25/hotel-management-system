from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt

from ui.new_reservation_dialog_ui import Ui_Dialog as NewReservationDialogUI


class NewReservationDialog(QDialog, NewReservationDialogUI):
    room_type_changed = pyqtSignal(str)
    room_changed = pyqtSignal(str)
    date_time_changed = pyqtSignal(str)
    spinbox_enabled = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.update_current_date_and_time()

        self.connect_signals_to_slots()

        self.current_page = 1

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
        frame.setObjectName(f"{service[1].replace(" ", "_")}_frame")

        h_layout = QHBoxLayout(frame)
        h_layout.setObjectName(f"{service[1].replace(" ", "_")}_h_layout")

        service_name_label = QLabel(parent=frame)
        service_name_label.setObjectName(f"{service[1].replace(" ", "_")}_label")
        service_name_label.setText(service[1])
        h_layout.addWidget(service_name_label)

        checkbox = QCheckBox(parent=frame)
        checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        checkbox.setText("")
        checkbox.setObjectName(f"{service[1].replace(" ", "_")}_checkbox")
        h_layout.addWidget(checkbox)

        spinbox = QSpinBox(parent=frame)
        spinbox.setObjectName(f"{service[1].replace(" ", "_")}_spinbox")
        spinbox.setEnabled(False)
        h_layout.addWidget(spinbox)

        checkbox.checkStateChanged.connect(lambda _, f=frame: self.enable_spinbox(f))

        frame.spinbox = spinbox
        frame.service = service
        frame.is_spinbox_enabled = False

        return frame

    def enable_spinbox(self, frame):
        if frame.spinbox.isEnabled():
            frame.spinbox.setEnabled(False)
            frame.is_spinbox_enabled = False
        else:
            frame.spinbox.setEnabled(True)
            frame.is_spinbox_enabled = True

        self.spinbox_enabled.emit()

    def connect_signals_to_slots(self):

        self.check_in_date_time_edit.dateTimeChanged.connect(self.update_check_out_date_time_edit_min_date)
        self.check_in_date_time_edit.dateTimeChanged.connect(lambda: self.date_time_changed.emit(self.rooms_combobox.currentText()))

        self.check_out_date_time_edit.dateTimeChanged.connect(lambda: self.date_time_changed.emit(self.rooms_combobox.currentText()))

        self.left_button.clicked.connect(lambda: self.page_change("left_button"))
        self.right_button.clicked.connect(lambda: self.page_change("right_button"))

        self.room_type_filter_combobox.currentTextChanged.connect(self.room_type_changed.emit)
        self.rooms_combobox.currentTextChanged.connect(self.room_changed.emit)

    def page_change(self, button_type):
        if self.current_page < 3 and button_type == "right_button":
            self.current_page += 1
        elif self.current_page >= 1 and button_type == "left_button":
            self.current_page -= 1

        # print(self.current_page)

        self.contents_stacked_widget.setCurrentIndex(self.current_page - 1)
