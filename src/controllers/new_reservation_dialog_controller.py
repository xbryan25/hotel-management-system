from PyQt6.QtWidgets import QSizePolicy, QSpacerItem

from models import AvailableRoomsModel, ServicesModel
from views import FeedbackDialog


class NewReservationDialogController:
    def __init__(self, dialog, db_driver):
        self.view = dialog
        self.db_driver = db_driver
        self.service_frames = []

        self.connect_signals_to_slots()

        self.set_models()

        self.create_service_frames(self.services_model.get_all())

    def connect_signals_to_slots(self):
        self.view.room_type_changed.connect(self.update_models)

        self.view.room_changed.connect(self.calculate_room_cost)
        self.view.date_time_changed.connect(self.calculate_room_cost)

        self.view.spinbox_enabled.connect(lambda: self.update_total_service_cost(self.service_frames))

        self.view.clicked_reservation.connect(self.make_reservation)

    def calculate_room_cost(self, current_room):
        check_in_check_out_date_time = self.view.get_check_in_check_out_date_and_time()

        seconds = check_in_check_out_date_time["check_in"].secsTo(check_in_check_out_date_time["check_out"])

        hours = seconds / 3600

        current_room_cost = self.available_room_numbers_model.get_cost_of_room(current_room)

        total_room_cost = (((hours-1)//24) + 1) * current_room_cost

        self.view.update_room_cost_value_label(total_room_cost)

    def update_total_service_cost(self, service_frames):

        total_services_cost = 0

        for service_frame in service_frames:
            if service_frame.is_spinbox_enabled:
                price = service_frame.service[2]
                quantity = service_frame.spinbox.value()
                total_services_cost += price * quantity

        self.view.update_service_cost_value_label(float(total_services_cost))

    def create_service_frames(self, services):
        for i in range(len(services)):
            frame = self.view.create_service_frame(services[i])

            self.view.services_scroll_area_grid_layout.addWidget(frame, i, 0, 1, 1)

            self.service_frames.append(frame)

            frame.spinbox.valueChanged.connect(lambda: self.update_total_service_cost(self.service_frames))

        v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.view.services_scroll_area_grid_layout.addItem(v_spacer, len(services), 0, 1, 1)

    def set_models(self):
        available_rooms = self.db_driver.get_available_rooms()

        # list(available_rooms) makes a copy of available_rooms so that it won't be affected
        self.available_room_numbers_model = AvailableRoomsModel(available_rooms, 0)
        self.available_room_types_model = AvailableRoomsModel(list(available_rooms), 1)

        self.view.rooms_combobox.setModel(self.available_room_numbers_model)

        self.view.room_type_filter_combobox.blockSignals(True)
        self.view.room_type_filter_combobox.setModel(self.available_room_types_model)
        self.view.room_type_filter_combobox.blockSignals(False)

        available_services = self.db_driver.get_all_services()
        self.services_model = ServicesModel(available_services)

    def update_models(self, room_type):

        if room_type == "-":
            available_rooms_from_room_type = self.db_driver.get_available_rooms()
        else:
            available_rooms_from_room_type = self.db_driver.get_available_rooms(room_type)

        self.available_room_numbers_model.set_rooms(available_rooms_from_room_type)

    def make_reservation(self):
        guest_inputs = self.view.get_guest_inputs()
        reservation_inputs = self.view.get_reservation_inputs()
        availed_services_inputs = self.view.get_availed_services_inputs(self.service_frames)

        self.db_driver.add_guest(guest_inputs)

        guest_id = self.db_driver.get_guest_id_from_name(guest_inputs["name"])
        reservation_inputs.update({"guest_id": guest_id})

        self.db_driver.add_reserved_room(reservation_inputs)
        self.db_driver.add_availed_services(availed_services_inputs, guest_id)

        self.success_dialog = FeedbackDialog("Reservation added successfully.", connected_view=self.view)
        self.success_dialog.exec()
