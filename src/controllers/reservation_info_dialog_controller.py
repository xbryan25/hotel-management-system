from PyQt6.QtWidgets import QSizePolicy, QSpacerItem
from PyQt6.QtCore import QDateTime

from models import AvailableRoomsModel, ServicesModel, AvailedServicesModel
from views import FeedbackDialog, ConfirmationDialog


class ReservationInfoDialogController:
    def __init__(self, dialog, db_driver, selected_reservation_id):
        self.view = dialog
        self.db_driver = db_driver
        self.selected_reservation_id = selected_reservation_id

        self.service_frames = []
        self.edit_state = False

        self.get_data_from_reservation()
        self.set_room_number_to_available_temporarily()
        self.set_models()
        self.load_data_from_reservation()

        self.create_service_frames(self.services_model.get_all())

        self.connect_signals_to_slots()

        self.temp_current_room = self.data_from_reservation[8]

        self.original_data = {
            'check_in_date': self.view.check_in_date_time_edit.dateTime(),
            'check_out_date': self.view.check_out_date_time_edit.dateTime(),
            'room_number': self.view.room_number_combobox.currentText(),
            'availed_services': self.services_model.get_all(),
            'total_reservation_cost': self.data_from_reservation[5]
        }

    def has_changes(self):
        current_data = {
            'check_in_date': self.view.check_in_date_time_edit.dateTime(),
            'check_out_date': self.view.check_out_date_time_edit.dateTime(),
            'room_number': self.view.room_number_combobox.currentText(),
            'availed_services': self.get_services_from_frames()
        }

        # Compare datetime
        if current_data['check_in_date'] != self.original_data['check_in_date']:
            self.view.enable_edit_reservation_button(True)
            return
        if current_data['check_out_date'] != self.original_data['check_out_date']:
            self.view.enable_edit_reservation_button(True)
            return

        # Compare selected room
        if current_data['room_number'] != self.original_data['room_number']:
            self.view.enable_edit_reservation_button(True)
            return

        # Compare availed services (you may need to sort or convert to set/dict)
        if current_data['availed_services'] != self.original_data['availed_services']:
            self.view.enable_edit_reservation_button(True)
            return

        self.view.enable_edit_reservation_button(False)

    def get_services_from_frames(self):
        services = []

        for service_frame in self.service_frames:
            services.append([service_frame.service_id, service_frame.service_name,
                             service_frame.spinbox.value(), service_frame.service_rate])

        return services

    def connect_signals_to_slots(self):
        self.view.room_type_changed.connect(self.update_models)

        self.view.room_changed.connect(lambda current_room: self.update_total_reservation_cost(current_room=current_room))
        self.view.room_changed.connect(self.has_changes)

        self.view.date_time_changed.connect(lambda current_room: self.update_total_reservation_cost(current_room=current_room))
        self.view.date_time_changed.connect(self.has_changes)

        self.view.clicked_edit_button.connect(lambda: self.enable_all_editable_fields(True))

        self.view.clicked_cancel_edit_button.connect(lambda: self.enable_all_editable_fields(False))

        self.view.clicked_cancel_reservation_button.connect(lambda: self.edit_or_cancel_reservation('cancel'))

        self.view.clicked_confirm_reservation_edit_button.connect(lambda: self.edit_or_cancel_reservation('edit'))

        self.view.spinbox_enabled.connect(self.update_total_reservation_cost)

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

        self.edit_state = state

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
            if service_frame.is_spinbox_enabled:
                price = service_frame.service_rate
                quantity = service_frame.spinbox.value()
                total_services_cost += price * quantity

        self.view.update_total_reservation_cost(total_room_cost + total_services_cost)

    def create_service_frames(self, services):
        self.view.clear_availed_services_layout()
        self.service_frames.clear()

        for i, service in enumerate(services):

            if self.availed_services_model.is_service_availed(service[0]):
                frame = self.view.create_service_frame(self.availed_services_model.get_availed_service_details(service[0]),
                                                       self.edit_state,
                                                       service_type='availed')
            else:
                frame = self.view.create_service_frame(service, self.edit_state)

            self.view.availed_services_scroll_area_grid_layout.addWidget(frame, i, 0, 1, 1)
            self.service_frames.append(frame)

            # lambda is used to not received the value given by valueChanged
            frame.spinbox.valueChanged.connect(lambda _: self.update_total_reservation_cost())
            frame.spinbox.valueChanged.connect(lambda _: self.has_changes())

            frame.checkbox.clicked.connect(lambda: print("clicked checkbox"))

            # frame.delete_push_button.clicked.connect(lambda _, f_id=frame.service_id,
            #                                          f_name=frame.service_name: self.delete_service(f_id, f_name))

        v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.view.availed_services_scroll_area_grid_layout.addItem(v_spacer, len(services), 0)

    def delete_service(self, service_id_to_delete, service_name_to_delete):
        self.confirmation_dialog = ConfirmationDialog(f"Confirm removal of {service_name_to_delete}?",
                                                      "This action cannot be undone.")

        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_choice():
            self.services_model.remove_service_by_id(service_id_to_delete)
            self.create_service_frames(self.services_model.get_all())
            self.update_total_reservation_cost()
            self.has_changes()

            self.success_dialog = FeedbackDialog("Service removed successfully.")
            self.success_dialog.exec()

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

        availed_services = self.db_driver.availed_service_queries.get_availed_services_from_avail_date(self.data_from_reservation[1])
        self.availed_services_model = AvailedServicesModel(availed_services)

        available_services = self.db_driver.service_queries.get_all_services()
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
