from PyQt6.QtWidgets import QSizePolicy, QSpacerItem
from PyQt6.QtCore import QDateTime

from models import AvailableRoomsModel, ServicesModel
from views import FeedbackDialog, ConfirmationDialog


class ReservationInfoDialogController:
    def __init__(self, dialog, db_driver, selected_reservation_id):
        self.view = dialog
        self.db_driver = db_driver
        self.selected_reservation_id = selected_reservation_id

        self.service_frames = []

        self.get_data_from_reservation()
        self.set_room_number_to_available_temporarily()
        self.set_models()
        self.load_data_from_reservation()

        self.create_service_frames(self.services_model.get_all())

        self.connect_signals_to_slots()

        self.temp_current_room = self.data_from_reservation[8]

    def connect_signals_to_slots(self):
        self.view.room_type_changed.connect(self.update_models)

        self.view.room_changed.connect(lambda current_room: self.update_total_reservation_cost(current_room=current_room))
        self.view.date_time_changed.connect(lambda current_room: self.update_total_reservation_cost(current_room=current_room))

        self.view.clicked_edit_button.connect(lambda: self.enable_all_editable_fields(True))

        self.view.clicked_cancel_edit_button.connect(lambda: self.enable_all_editable_fields(False))

        self.view.clicked_cancel_reservation_button.connect(lambda: self.edit_or_cancel_reservation('cancel'))

        self.view.clicked_confirm_reservation_edit_button.connect(lambda: self.edit_or_cancel_reservation('edit'))

    def edit_or_cancel_reservation(self, state):

        if state == 'cancel':
            self.confirmation_dialog = ConfirmationDialog(f"Confirm cancellation of {self.selected_reservation_id}?",
                                                          "This action cannot be undone.")

            self.confirmation_dialog.exec()

            if self.confirmation_dialog.get_choice():
                self.feedback_dialog = FeedbackDialog("Reservation cancelled successfully.", connected_view=self.view)
                self.feedback_dialog.exec()

                # Then refresh reservation table

        else:
            self.confirmation_dialog = ConfirmationDialog(f"Confirm reservation edit of {self.selected_reservation_id}?")

            self.confirmation_dialog.exec()

            if self.confirmation_dialog.get_choice():
                self.feedback_dialog = FeedbackDialog("Reservation edited successfully.", connected_view=self.view)
                self.feedback_dialog.exec()

                # Then refresh reservation table

    def enable_all_editable_fields(self, state):
        self.view.enable_all_editable_fields(self.service_frames, state)

    def update_total_reservation_cost(self, current_room=None):

        # Room section
        if current_room:
            self.temp_current_room = current_room

        check_in_check_out_date_time = self.view.get_check_in_check_out_date_and_time()

        seconds = check_in_check_out_date_time["check_in"].secsTo(check_in_check_out_date_time["check_out"])

        hours = seconds / 3600

        current_room_cost = self.available_room_numbers_model.get_cost_of_room(self.temp_current_room)

        total_room_cost = (((hours-1)//24) + 1) * current_room_cost

        # Services section

        total_services_cost = 0

        for service_frame in self.service_frames:
            price = service_frame.service[3]
            quantity = service_frame.spinbox.value()
            total_services_cost += price * quantity

        self.view.update_total_reservation_cost(total_room_cost + total_services_cost)

    # def update_total_service_cost(self, service_frames):
    #
    #     total_services_cost = 0
    #
    #     for service_frame in service_frames:
    #         if service_frame.is_spinbox_enabled:
    #             price = service_frame.service[2]
    #             quantity = service_frame.spinbox.value()
    #             total_services_cost += price * quantity
    #
    #     self.view.update_service_cost_value_label(float(total_services_cost))

    def create_service_frames(self, services):
        for i in range(len(services)):
            frame = self.view.create_service_frame(services[i])

            self.view.availed_services_scroll_area_grid_layout.addWidget(frame, i, 0, 1, 1)

            self.service_frames.append(frame)

            # lambda is used to not received the value given by valueChanged
            frame.spinbox.valueChanged.connect(lambda _: self.update_total_reservation_cost())

        v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.view.availed_services_scroll_area_grid_layout.addItem(v_spacer, len(services), 0, 1, 1)

    def get_data_from_reservation(self):
        self.data_from_reservation = self.db_driver.reserved_room_queries.get_reservation_details(
            self.selected_reservation_id)

    def set_room_number_to_available_temporarily(self):
        self.db_driver.room_queries.set_room_status(self.data_from_reservation[8], "available", set_type="temporary")

    def load_data_from_reservation(self):

        guest_name = self.db_driver.guest_queries.get_name_from_guest_id(self.data_from_reservation[7])
        room_type = self.db_driver.room_queries.get_room_type(self.data_from_reservation[8])

        self.view.reservation_id_value_label.setText(self.selected_reservation_id)
        self.view.reservation_status_value_label.setText(self.data_from_reservation[6])
        self.view.payment_status_value_label.setText(self.data_from_reservation[4])
        self.view.total_reservation_cost_value_label.setText(f"₱{self.data_from_reservation[5]}")

        self.view.guest_id_value_label.setText(self.data_from_reservation[7])
        self.view.guest_name_value_label.setText(guest_name)

        self.view.check_in_date_time_edit.setDateTime(QDateTime(self.data_from_reservation[2]))
        self.view.check_out_date_time_edit.setDateTime(QDateTime(self.data_from_reservation[3]))

        self.view.remaining_balance_value_label.setText(f"₱{self.data_from_reservation[9]}")

        self.view.room_number_combobox.setCurrentText(self.data_from_reservation[8])
        self.view.room_type_combobox.setCurrentText(room_type)

    def set_models(self):
        # TODO: Set current room to be temporarily 'available' for it to get caught by query

        available_rooms = self.db_driver.room_queries.get_available_rooms()

        # list(available_rooms) makes a copy of available_rooms so that it won't be affected
        self.available_room_numbers_model = AvailableRoomsModel(available_rooms, 0)
        self.available_room_types_model = AvailableRoomsModel(list(available_rooms), 1)

        self.view.room_number_combobox.setModel(self.available_room_numbers_model)

        self.view.room_type_combobox.blockSignals(True)
        self.view.room_type_combobox.setModel(self.available_room_types_model)
        self.view.room_type_combobox.blockSignals(False)

        available_services = self.db_driver.availed_service_queries.get_availed_services_from_avail_date(self.data_from_reservation[1])
        self.services_model = ServicesModel(available_services)

    def update_models(self, room_type):

        if room_type == "-":
            available_rooms_from_room_type = self.db_driver.room_queries.get_available_rooms()
        else:
            available_rooms_from_room_type = self.db_driver.room_queries.get_available_rooms(room_type)

        self.available_room_numbers_model.set_rooms(available_rooms_from_room_type)

    # def make_reservation(self):
    #     guest_inputs = self.view.get_guest_inputs()
    #     reservation_inputs = self.view.get_reservation_inputs()
    #     availed_services_inputs = self.view.get_availed_services_inputs(self.service_frames)
    #
    #     room_number = reservation_inputs["room_number"]
    #
    #     self.db_driver.guest_queries.add_guest(guest_inputs)
    #
    #     guest_id = self.db_driver.guest_queries.get_guest_id_from_name(guest_inputs["name"])
    #     reservation_inputs.update({"guest_id": guest_id})
    #
    #     self.db_driver.reserved_room_queries.add_reserved_room(reservation_inputs)
    #     self.db_driver.availed_service_queries.add_availed_services(availed_services_inputs, guest_id)
    #
    #     self.db_driver.room_queries.set_room_status(room_number, 'reserved')
    #
    #     self.success_dialog = FeedbackDialog("Reservation added successfully.", connected_view=self.view)
    #     self.success_dialog.exec()
