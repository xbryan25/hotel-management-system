from PyQt6.QtWidgets import QSizePolicy, QSpacerItem

from views import FeedbackDialog


class AddPaymentDialogController:
    def __init__(self, dialog, db_driver, data_from_row):
        self.view = dialog
        self.db_driver = db_driver
        self.data_from_row = data_from_row

        self.connect_signals_to_slots()

        self.setup_view()

    def connect_signals_to_slots(self):
        self.view.clicked_add_payment_button.connect(self.make_payment)

    def setup_view(self):
        self.view.set_remaining_balance_value(self.data_from_row['remaining_balance'])
        self.view.set_spinbox_max_value(self.data_from_row['remaining_balance'])

    def make_payment(self):
        payment_inputs = self.view.get_payment_inputs()

        payment_inputs.update({'guest_id': self.db_driver.reserved_room_queries.get_specific_reservation_details('guest_id', self.data_from_row['reservation_id'])})

        payment_inputs.update({'room_id': self.db_driver.reserved_room_queries.get_specific_reservation_details('room_id', self.data_from_row['reservation_id'])})

        self.db_driver.paid_room_queries.add_paid_room(payment_inputs)

        if self.data_from_row['remaining_balance'] == payment_inputs['amount']:
            self.db_driver.reserved_room_queries.set_payment_status(self.data_from_row['reservation_id'], 'fully paid')
        elif self.data_from_row['remaining_balance'] > payment_inputs['amount']:
            self.db_driver.reserved_room_queries.set_payment_status(self.data_from_row['reservation_id'], 'partially paid')

        self.success_dialog = FeedbackDialog("Payment added successfully.", connected_view=self.view)
        self.success_dialog.exec()
