from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt

from ui.new_reservation_dialog_ui import Ui_Dialog as NewReservationDialogUI


class NewReservationDialog(QDialog, NewReservationDialogUI):
    room_type_changed = pyqtSignal(str)
    room_changed = pyqtSignal(str)
    date_time_changed = pyqtSignal(str)

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

    def update_total_cost_value_label(self):
        room_cost = float(self.room_cost_value_label.text())

        self.total_cost_value_label.setText(str(room_cost))

    def load_services_frames(self, services):

        for i in range(len(services)):
            temp_frame = QFrame(parent=self.services_scroll_area_contents)
            temp_frame.setFrameShape(QFrame.Shape.StyledPanel)
            temp_frame.setFrameShadow(QFrame.Shadow.Raised)
            temp_frame.setObjectName("temp_frame")

            horizontalLayout_2 = QHBoxLayout(temp_frame)
            horizontalLayout_2.setObjectName("horizontalLayout_2")

            temp_label = QLabel(parent=temp_frame)
            temp_label.setObjectName("temp_label")
            temp_label.setText(services[i][1])

            horizontalLayout_2.addWidget(temp_label)
            temp_checkbox = QCheckBox(parent=temp_frame)
            temp_checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            temp_checkbox.setText("")
            temp_checkbox.setObjectName("temp_checkbox")

            horizontalLayout_2.addWidget(temp_checkbox)
            temp_spinbox = QSpinBox(parent=temp_frame)
            temp_spinbox.setObjectName("temp_spinbox")
            temp_spinbox.setEnabled(False)
            horizontalLayout_2.addWidget(temp_spinbox)

            temp_checkbox.checkStateChanged.connect(lambda _, s=temp_spinbox: self.enable_spinbox(s))

            self.services_scroll_area_grid_layout.addWidget(temp_frame, i, 0, 1, 1)

        spacerItem5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                            QSizePolicy.Policy.Expanding)
        self.services_scroll_area_grid_layout.addItem(spacerItem5, len(services), 0, 1, 1)

    @staticmethod
    def enable_spinbox(spinbox):
        if spinbox.isEnabled():
            spinbox.setEnabled(False)
        else:
            spinbox.setEnabled(True)


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
