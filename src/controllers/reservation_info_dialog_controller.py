from PyQt6.QtWidgets import QSizePolicy, QSpacerItem
from PyQt6.QtCore import QDateTime

from models import RoomsModel, ServicesModel, AvailedServicesModel
from views import FeedbackDialog, ConfirmationDialog, UpcomingReservationsDialog
from controllers.upcoming_reservations_dialog_controller import UpcomingReservationsDialogController

from datetime import datetime


class ReservationInfoDialogController:
    def __init__(self, dialog, db_driver, selected_reservation_id, view_type='current'):
        self.view = dialog
        self.db_driver = db_driver
        self.selected_reservation_id = selected_reservation_id
        self.view_type = view_type

        self.service_frames = []
        self.edit_state = False

        self.get_data_from_reservation()

        if self.view_type != 'current':
            self.setup_past_view_mode()

        self.original_room_number = self.db_driver.room_queries.get_room_number_from_room_id(
            self.data_from_reservation['room_id'])

        self.temp_current_room = self.original_room_number

        self.set_models()
        self.load_data_from_reservation()

        self.create_service_frames(self.services_model.get_all())

        self.connect_signals_to_slots()

        self.view.update_current_date_and_time(self.data_from_reservation['check_in_date'],
                                               self.data_from_reservation['check_out_date'],
                                               mode='same_room')

    def check_reservation_dates(self):
        current_check_in_date = self.data_from_reservation['check_in_date']
        current_check_out_date = self.data_from_reservation['check_out_date']

        new_check_in_date = self.view.check_in_date_time_edit.dateTime().toPyDateTime()
        new_check_out_date = self.view.check_out_date_time_edit.dateTime().toPyDateTime()

        room_id = self.db_driver.room_queries.get_room_id_from_room_number(self.view.room_number_combobox.currentText())

        reservation_durations = self.db_driver.reserved_room_queries.get_all_check_in_and_check_out_of_room(room_id)

        has_overlap = False

        for existing_check_in, existing_check_out in reservation_durations:

            # Skip the current reservation
            if existing_check_in == current_check_in_date and existing_check_out == current_check_out_date:
                continue

            # Check for overlap
            if new_check_in_date < existing_check_out and new_check_out_date > existing_check_in:

                self.conflict_dialog = FeedbackDialog("Reservation conflict found.",
                                                      f"Please recheck the reservations of '{self.view.room_number_combobox.currentText()}'.")
                self.conflict_dialog.exec()

                has_overlap = True
                break

        if not has_overlap:
            self.edit_or_cancel_reservation('edit')

    def open_upcoming_reservations_dialog(self):

        self.upcoming_reservations_dialog = UpcomingReservationsDialog()
        self.upcoming_reservations_dialog_controller = UpcomingReservationsDialogController(self.upcoming_reservations_dialog,
                                                                                            self.db_driver,
                                                                                            self.view.room_number_combobox.currentText())

        self.upcoming_reservations_dialog.exec()

    def has_changes(self):
        current_data = {
            'check_in_date': self.view.check_in_date_time_edit.dateTime(),
            'check_out_date': self.view.check_out_date_time_edit.dateTime(),
            'room_number': self.view.room_number_combobox.currentText(),
            'availed_services': self.get_services_from_frames()
        }

        # Compare datetime
        if current_data['check_in_date'] != self.data_from_reservation['check_in_date']:
            self.view.enable_edit_reservation_button(True)
            return
        if current_data['check_out_date'] != self.data_from_reservation['check_out_date']:
            self.view.enable_edit_reservation_button(True)
            return

        # Compare selected room
        if current_data['room_number'] != self.original_room_number:
            self.view.enable_edit_reservation_button(True)
            return

        if self.compare_current_and_original_availed_services(current_data['availed_services']):
            self.view.enable_edit_reservation_button(True)
            return

        self.view.enable_edit_reservation_button(False)

    def compare_current_and_original_availed_services(self, current_availed_services):
        if not current_availed_services and self.availed_services_model.get_all():
            return True
        elif len(current_availed_services) != len(self.availed_services_model.get_all()):
            return True

        for current_availed_service in current_availed_services:
            availed_service_details = self.availed_services_model.get_availed_service_details(current_availed_service[0])

            if not availed_service_details:
                return True
            elif availed_service_details[2] != current_availed_service[2]:
                return True

        return False

    def get_services_from_frames(self):
        services = []

        for service_frame in self.service_frames:
            if service_frame.is_spinbox_enabled:
                services.append([service_frame.service_id, service_frame.service_name,
                                 service_frame.spinbox.value(), service_frame.service_rate])

        return services

    def connect_signals_to_slots(self):

        if self.view_type == 'current':
            self.view.room_type_changed.connect(self.update_models)

            self.view.room_changed.connect(self.update_current_date_and_time)
            self.view.room_changed.connect(lambda current_room: self.update_total_reservation_cost(current_room=current_room))
            self.view.room_changed.connect(self.has_changes)

            self.view.date_time_changed.connect(lambda current_room: self.update_total_reservation_cost(current_room=current_room))
            self.view.date_time_changed.connect(self.has_changes)

            self.view.clicked_edit_button.connect(lambda: self.enable_all_editable_fields(True))

            self.view.clicked_cancel_edit_button.connect(lambda: self.enable_all_editable_fields(False))

            self.view.clicked_cancel_reservation_button.connect(lambda: self.edit_or_cancel_reservation('cancel'))

            self.view.clicked_confirm_reservation_edit_button.connect(self.check_reservation_dates)

            self.view.spinbox_enabled.connect(self.update_total_reservation_cost)
            self.view.spinbox_enabled.connect(self.has_changes)

            self.view.room_reservations_button.clicked.connect(self.open_upcoming_reservations_dialog)

        else:
            self.view.room_reservations_button.clicked.connect(self.open_upcoming_reservations_dialog)

            self.view.clicked_proceed_button.connect(self.view.close)

    def update_current_date_and_time(self, room_number):
        if room_number != self.original_room_number:
            self.view.update_current_date_and_time(mode='different_room')
        else:
            self.view.update_current_date_and_time(self.data_from_reservation['check_in_date'],
                                                   self.data_from_reservation['check_out_date'],
                                                   mode='same_room')

    def edit_or_cancel_reservation(self, state):

        if state == 'cancel':

            # Cancel reservation

            self.confirmation_dialog = ConfirmationDialog(f"Confirm cancellation of {self.selected_reservation_id}?",
                                                          "This action cannot be undone.")

            self.confirmation_dialog.exec()

            if self.confirmation_dialog.get_choice():

                self.db_driver.reserved_room_queries.set_reservation_status('Cancelled', self.selected_reservation_id)
                # self.db_driver.room_queries.set_room_status(self.original_data["room_number"], "available")

                amount_already_paid = self.data_from_reservation['total_reservation_cost'] - self.data_from_reservation['remaining_balance']

                if amount_already_paid > 0:
                    self.feedback_dialog = FeedbackDialog("Since payments have been done,",
                                                          f"the refund will be ₱{amount_already_paid}.")
                    self.feedback_dialog.exec()

                    self.db_driver.paid_room_queries.add_paid_room({'payment_type': 'Cash',
                                                                    'amount': amount_already_paid * -1,
                                                                    'transaction_date': datetime.now(),
                                                                    'guest_id': self.data_from_reservation['guest_id'],
                                                                    'room_id': self.data_from_reservation['room_id']})

                self.feedback_dialog = FeedbackDialog("Reservation cancelled successfully.", connected_view=self.view)
                self.feedback_dialog.exec()

        else:

            # Edit reservation

            self.confirmation_dialog = ConfirmationDialog(f"Confirm reservation edit of {self.selected_reservation_id}?")

            self.confirmation_dialog.exec()

            if self.confirmation_dialog.get_choice():

                reservation_inputs = self.view.get_reservation_inputs()
                modified_availed_services_inputs = self.view.get_modified_availed_services_inputs(self.service_frames)
                new_availed_services_inputs = self.view.get_new_availed_services_inputs(self.service_frames)
                room_id = self.db_driver.room_queries.get_room_id_from_room_number(reservation_inputs["room_number"])

                date_time_now = datetime.now()

                reservation_inputs.update({"room_id": room_id})

                self.db_driver.availed_service_queries.update_availed_services(modified_availed_services_inputs,
                                                                               date_time_now)

                self.db_driver.availed_service_queries.add_availed_services(new_availed_services_inputs,
                                                                            self.data_from_reservation['guest_id'],
                                                                            date_time_now)

                self.db_driver.reserved_room_queries.update_reserved_room(self.selected_reservation_id,
                                                                          reservation_inputs,
                                                                          date_time_now)

                new_total = int(reservation_inputs['total_reservation_cost'])
                amount_already_paid = self.data_from_reservation['total_reservation_cost'] - self.data_from_reservation['remaining_balance']

                if amount_already_paid > 0 and amount_already_paid != self.data_from_reservation['total_reservation_cost']:
                    self.db_driver.reserved_room_queries.set_payment_status(self.selected_reservation_id, 'Partially Paid')
                elif amount_already_paid == 0:
                    self.db_driver.reserved_room_queries.set_payment_status(self.selected_reservation_id,
                                                                            'Not Paid')

                # For refund
                if new_total < amount_already_paid:
                    amount_to_refund = amount_already_paid - new_total

                    self.feedback_dialog = FeedbackDialog("Total amount paid is greater than new total.",
                                                          f"The refund will be ₱{amount_to_refund}.")
                    self.feedback_dialog.exec()

                    self.db_driver.paid_room_queries.add_paid_room({'payment_type': 'Cash',
                                                                    'amount': amount_to_refund * -1,
                                                                    'transaction_date': date_time_now,
                                                                    'guest_id': self.data_from_reservation['guest_id'],
                                                                    'room_id': self.data_from_reservation['room_id']})

                    self.db_driver.reserved_room_queries.set_payment_status(self.selected_reservation_id, 'Fully Paid')

                if self.original_room_number != reservation_inputs["room_number"]:

                    # TODO: Cancel reservation
                    pass


                    # # Set old room number to 'available'
                    # self.set_room_number_to_available()
                    #
                    # # Set new room number to be 'reserved'
                    # self.db_driver.room_queries.set_room_status(reservation_inputs["room_number"], "reserved")

                self.feedback_dialog = FeedbackDialog("Reservation edited successfully.", connected_view=self.view)
                self.feedback_dialog.exec()

                # Then refresh reservation table

    def enable_all_editable_fields(self, state):
        self.view.enable_all_editable_fields(self.service_frames, state)

        self.edit_state = state

    def setup_past_view_mode(self):
        # booking = self.db_driver.booked_rooms_queries.find_booking_by_guest_and_room()

        self.view.load_proceed_button()
        self.view.hide_remaining_balance()
        # self.view.load_booking_details()

    def update_total_reservation_cost(self, current_room=None):

        # Room section
        if current_room:
            self.temp_current_room = current_room

        check_in_check_out_date_time = self.view.get_check_in_check_out_date_and_time()

        seconds = check_in_check_out_date_time["check_in"].secsTo(check_in_check_out_date_time["check_out"])

        hours = seconds / 3600

        current_room_cost = self.room_numbers_model.get_cost_of_room(self.temp_current_room)

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
            is_service_availed = self.availed_services_model.is_service_availed(service[0])
            is_service_active = self.db_driver.service_queries.get_service_active_status(service[0])

            if not is_service_availed and not is_service_active:
                continue

            if is_service_availed:
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

    def load_data_from_reservation(self):

        guest_name = self.db_driver.guest_queries.get_name_from_guest_id(self.data_from_reservation['guest_id'])
        room_type = self.db_driver.room_queries.get_room_type(self.original_room_number)

        self.view.reservation_id_value_label.setText(self.selected_reservation_id)
        self.view.reservation_status_value_label.setText(self.data_from_reservation['reservation_status'])
        self.view.payment_status_value_label.setText(self.data_from_reservation['payment_status'])
        self.view.total_reservation_cost_value_label.setText(f"₱{self.data_from_reservation['total_reservation_cost']}")

        self.view.guest_id_value_label.setText(self.data_from_reservation['guest_id'])
        self.view.guest_name_value_label.setText(guest_name)

        self.view.check_in_date_time_edit.setDateTime(QDateTime(self.data_from_reservation['check_in_date']))
        self.view.check_out_date_time_edit.setDateTime(QDateTime(self.data_from_reservation['check_out_date']))

        self.view.remaining_balance_value_label.setText(f"₱{self.data_from_reservation['remaining_balance']}")

        self.view.room_number_combobox.setCurrentText(self.original_room_number)
        self.view.room_type_combobox.setCurrentText(room_type)

    def set_models(self):
        all_rooms = self.db_driver.room_queries.get_all_rooms(enable_pagination=False)

        self.room_numbers_model = RoomsModel(all_rooms, model_type='nrd_room_numbers')
        self.room_types_model = RoomsModel(all_rooms, model_type='nrd_room_types')

        self.view.room_number_combobox.setModel(self.room_numbers_model)

        self.view.room_type_combobox.blockSignals(True)
        self.view.room_type_combobox.setModel(self.room_types_model)
        self.view.room_type_combobox.blockSignals(False)

        availed_services = self.db_driver.availed_service_queries.get_availed_services_from_avail_date(self.data_from_reservation['last_modified'])
        self.availed_services_model = AvailedServicesModel(availed_services)

        all_services = self.db_driver.service_queries.get_all_services(view_type="All")
        self.services_model = ServicesModel(all_services)

    def update_models(self, room_type):

        if room_type == "-":
            rooms_from_room_type = self.db_driver.room_queries.get_all_rooms(enable_pagination=False)
        else:
            rooms_from_room_type = self.db_driver.room_queries.get_rooms_from_room_type(room_type)

        self.room_numbers_model.update_data(rooms_from_room_type)
