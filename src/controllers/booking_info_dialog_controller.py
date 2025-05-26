from PyQt6.QtWidgets import QSizePolicy, QSpacerItem
from PyQt6.QtCore import QDateTime

from models import ServicesModel, AvailedServicesModel

from datetime import datetime


class BookingInfoDialogController:
    def __init__(self, dialog, db_driver, selected_booking_id):
        self.view = dialog
        self.db_driver = db_driver
        self.selected_booking_id = selected_booking_id

        self.service_frames = []

        self.get_data_from_booking()

        self.set_models()
        self.load_data_from_booking()

        # self.connect_signals_to_slots()

        self.create_service_frames(self.services_model.get_all())

    def connect_signals_to_slots(self):
        pass

    def create_service_frames(self, services):
        self.view.clear_availed_services_layout()
        self.service_frames.clear()

        for i, service in enumerate(services):
            is_service_availed = self.availed_services_model.is_service_availed(service[0])
            is_service_active = self.db_driver.service_queries.get_service_active_status(service[0])

            if not is_service_availed and not is_service_active:
                continue

            if is_service_availed:
                frame = self.view.create_service_frame(self.availed_services_model.get_availed_service_details(service[0]),
                                                       service_type='availed')
            else:
                frame = self.view.create_service_frame(service)

            self.view.availed_services_scroll_area_grid_layout.addWidget(frame, i, 0, 1, 1)
            self.service_frames.append(frame)

            # lambda is used to not received the value given by valueChanged
            # frame.spinbox.valueChanged.connect(lambda _: self.update_total_reservation_cost())
            # frame.spinbox.valueChanged.connect(lambda _: self.has_changes())

            # frame.delete_push_button.clicked.connect(lambda _, f_id=frame.service_id,
            #                                          f_name=frame.service_name: self.delete_service(f_id, f_name))

        v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.view.availed_services_scroll_area_grid_layout.addItem(v_spacer, len(services), 0)

    def get_data_from_booking(self):
        self.data_from_booking = self.db_driver.booked_room_queries.get_booking_details(self.selected_booking_id)

    def load_data_from_booking(self):

        self.view.booking_id_value_label.setText(self.selected_booking_id)
        self.view.check_in_status_value_label.setText(self.data_from_booking['check_in_status'])

        self.view.reservation_id_value_label.setText(self.data_from_booking['reservation_id'])
        self.view.total_reservation_cost_value_label.setText(f"₱{self.data_from_booking['total_reservation_cost']}")

        self.view.check_in_date_value_label.setText(self.data_from_booking['check_in_date'].strftime("%B %d, %Y %I:%M %p"))
        self.view.check_out_date_value_label.setText(self.data_from_booking['check_out_date'].strftime("%B %d, %Y %I:%M %p"))
        self.view.actual_check_in_date_value_label.setText(self.data_from_booking['actual_check_in_date'].strftime("%B %d, %Y %I:%M %p"))
        self.view.actual_check_out_date_value_label.setText(self.data_from_booking['actual_check_out_date'].strftime("%B %d, %Y %I:%M %p")
                                                            if self.data_from_booking['actual_check_out_date'] else "-")

        self.view.guest_id_value_label.setText(self.data_from_booking['guest_id'])
        self.view.room_type_value_label.setText(self.data_from_booking['room_type'])
        self.view.guest_name_value_label.setText(self.truncate_text(self.data_from_booking['name']))
        self.view.room_number_value_label.setText(self.data_from_booking['room_number'])
        self.view.guest_count_value_label.setText(str(self.data_from_booking['guest_count']))

    def set_models(self):
        availed_services = self.db_driver.availed_service_queries.get_availed_services_from_avail_date(self.data_from_booking['last_modified'])
        self.availed_services_model = AvailedServicesModel(availed_services)

        all_services = self.db_driver.service_queries.get_all_services(view_type="All")
        self.services_model = ServicesModel(all_services)

    @staticmethod
    def truncate_text(text, max_length=35):
        if len(text) <= max_length:
            return text
        return name[:max_length - 3] + "..."
