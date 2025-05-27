from PyQt6.QtWidgets import QDialog, QSpacerItem, QFrame, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QSpinBox, QPushButton
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import pyqtSignal, QDateTime, Qt, QSize

from datetime import datetime

from ui import BookingInfoDialogUI


class BookingInfoDialog(QDialog, BookingInfoDialogUI):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_signals_to_slots()

        self.load_fonts()
        self.set_external_stylesheet()

        self.setWindowTitle("HotelEase | Booking Information")

    def create_service_frame(self, service, edit_state=False, service_type='not availed'):
        # TODO: Make into another file, I guess?

        frame = QFrame(parent=self.availed_services_scroll_area_widget_contents)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame_object_name = f"{service[1].replace(" ", "_")}_frame"
        frame.setObjectName(frame_object_name)

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

            frame.setStyleSheet(f"#{frame_object_name}{{background-color: #c0c0c0; border: 1px solid #d9d9d9;}}")

        elif service_type == 'not availed':
            frame.service_rate = service[2]
            frame.is_spinbox_enabled = False
            frame.avail_id = None

            frame.setStyleSheet(f"#{frame_object_name}{{background-color: transparent; border: 1px solid #d9d9d9;}}")

        return frame

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

    def connect_signals_to_slots(self):

        self.proceed_button.clicked.connect(self.close)

    def set_external_stylesheet(self):
        with open("../resources/styles/booking_info_dialog.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):

        self.bookings_details_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.proceed_button.setFont(QFont("Inter", 15, QFont.Weight.Bold))

        self.booking_id_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.booking_id_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.check_in_status_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.check_in_status_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.reservation_id_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.reservation_id_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.total_reservation_cost_label.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        self.total_reservation_cost_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.check_in_date_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.check_in_date_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.check_out_date_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.check_out_date_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.actual_check_in_date_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.actual_check_in_date_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.actual_check_out_date_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.actual_check_out_date_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.guest_id_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.guest_id_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_type_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_type_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.guest_name_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.guest_name_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.room_number_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.room_number_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.guest_count_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.guest_count_value_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.availed_services_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
