from PyQt6.QtWidgets import QSizePolicy, QSpacerItem

from models import RoomsModel, ServicesModel
from views import FeedbackDialog, UpcomingReservationsDialog
from controllers.upcoming_reservations_dialog_controller import UpcomingReservationsDialogController

import math


class NewReservationDialogController:
    def __init__(self, dialog, db_driver):
        self.view = dialog
        self.db_driver = db_driver
        self.service_frames = []

        self.connect_signals_to_slots()

        self.set_models()

        self.create_service_frames(self.services_model.get_all())

    def open_upcoming_reservations_dialog(self):

        self.upcoming_reservations_dialog = UpcomingReservationsDialog()
        self.upcoming_reservations_dialog_controller = UpcomingReservationsDialogController(self.upcoming_reservations_dialog,
                                                                                            self.db_driver,
                                                                                            self.view.rooms_combobox.currentText())

        self.upcoming_reservations_dialog.exec()

    def connect_signals_to_slots(self):
        self.view.room_type_changed.connect(self.update_models)

        self.view.room_changed.connect(self.calculate_room_cost)
        self.view.date_time_changed.connect(self.calculate_room_cost)

        self.view.spinbox_enabled.connect(lambda: self.update_total_service_cost(self.service_frames))

        self.view.clicked_reservation.connect(self.make_reservation)

        self.view.room_reservations_button.clicked.connect(self.open_upcoming_reservations_dialog)

        self.view.selected_reservation_duration.connect(self.check_reservation_dates)

    def check_reservation_dates(self, new_check_in_date, new_check_out_date):
        room_id = self.db_driver.room_queries.get_room_id_from_room_number(self.view.rooms_combobox.currentText())

        reservation_durations = self.db_driver.reserved_room_queries.get_all_check_in_and_check_out_of_room(room_id)

        has_overlap = False

        for reservation_duration in reservation_durations:

            # Coincide
            if ((reservation_duration[0] < new_check_in_date and reservation_duration[1] > new_check_out_date) or
                    (new_check_in_date < reservation_duration[0] < new_check_out_date) or
                    (reservation_duration[0] < new_check_in_date < reservation_duration[1])):

                self.conflict_dialog = FeedbackDialog("Reservation conflict found.",
                                                      f"Please recheck the reservations of '{self.view.rooms_combobox.currentText()}'.")
                self.conflict_dialog.exec()

                has_overlap = True
                break

        if not has_overlap:
            self.view.page_change("right_button")

    def calculate_room_cost(self, current_room):
        check_in_check_out_date_time = self.view.get_check_in_check_out_date_and_time()

        seconds = check_in_check_out_date_time["check_in"].secsTo(check_in_check_out_date_time["check_out"])

        hours = seconds / 3600

        current_room_cost = self.room_numbers_model.get_cost_of_room(current_room)

        if hours % 24 == 0:
            total_room_cost = (((hours - 1) // 24) + 1) * current_room_cost
        else:
            total_room_cost = float(math.ceil((((hours - 1) / 24) + 1) * current_room_cost))

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
        all_rooms = self.db_driver.room_queries.get_all_rooms(enable_pagination=False)

        self.room_numbers_model = RoomsModel(all_rooms, model_type='nrd_room_numbers')
        self.room_types_model = RoomsModel(all_rooms, model_type='nrd_room_types')

        self.view.rooms_combobox.setModel(self.room_numbers_model)

        self.view.room_type_filter_combobox.blockSignals(True)
        self.view.room_type_filter_combobox.setModel(self.room_types_model)
        self.view.room_type_filter_combobox.blockSignals(False)

        available_services = self.db_driver.service_queries.get_all_services()
        self.services_model = ServicesModel(available_services)

    def update_models(self, room_type):

        if room_type == "-":
            rooms_from_room_type = self.db_driver.room_queries.get_all_rooms(enable_pagination=False)
        else:
            rooms_from_room_type = self.db_driver.room_queries.get_rooms_from_room_type(room_type)

        self.room_numbers_model.update_data(rooms_from_room_type)

    def make_reservation(self):
        guest_inputs = self.view.get_guest_inputs()
        reservation_inputs = self.view.get_reservation_inputs()
        availed_services_inputs = self.view.get_availed_services_inputs(self.service_frames)

        self.db_driver.guest_queries.add_guest(guest_inputs)

        guest_id = self.db_driver.guest_queries.get_guest_id_from_name(guest_inputs["name"])
        room_id = self.db_driver.room_queries.get_room_id_from_room_number(reservation_inputs["room_number"])

        reservation_inputs.update({"guest_id": guest_id})
        reservation_inputs.update({"room_id": room_id})

        self.db_driver.reserved_room_queries.add_reserved_room(reservation_inputs)
        self.db_driver.availed_service_queries.add_availed_services(availed_services_inputs, guest_id)

        # self.db_driver.room_queries.set_room_status(room_number, 'reserved')

        self.success_dialog = FeedbackDialog("Reservation added successfully.", connected_view=self.view)
        self.success_dialog.exec()
