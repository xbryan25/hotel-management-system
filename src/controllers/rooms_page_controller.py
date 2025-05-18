from PyQt6.QtCore import QTimer

from models import RoomsModel
from views import AddEditRoomDialog, ConfirmationDialog, FeedbackDialog
from controllers.add_edit_room_dialog_controller import AddEditRoomDialogController


class RoomsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.rooms_model = None

        self.view_mode = "list_view"

        self.set_models()

        self.connect_signals_to_slots()

        self.load_frames()
        self.load_data()

    def set_models(self):
        rooms_data = self.db_driver.room_queries.get_all_rooms()

        # Only for list view
        initial_rows = self.view.get_list_view_current_max_rows()

        if not self.rooms_model:
            self.rooms_model = RoomsModel(rooms_data, initial_rows, -1)
        else:
            self.rooms_model.update_data(rooms_data)

    def load_frames(self):
        if self.view_mode == "list_view":
            self.view.make_list_view_rooms_frame(self.rooms_model.get_per_page(self.view_mode))
        else:
            self.view.make_grid_view_rooms_frame(self.rooms_model.get_per_page(self.view_mode))

    def load_data(self):
        if self.view_mode == "list_view":
            self.view.update_list_view_frames_contents(self.rooms_model.get_rooms_from_current_page(self.view_mode),
                                                       self.open_add_edit_room_dialog, self.delete_room)
        else:
            self.view.update_grid_view_frames_contents(self.rooms_model.get_rooms_from_current_page(self.view_mode),
                                                       self.open_add_edit_room_dialog, self.delete_room)

    def open_add_edit_room_dialog(self, dialog_type, room_number=None):
        self.add_edit_room_dialog = AddEditRoomDialog()
        self.add_edit_room_dialog_controller = AddEditRoomDialogController(self.add_edit_room_dialog, self.db_driver,
                                                                           dialog_type, room_number)

        self.add_edit_room_dialog.exec()

        self.set_models()
        self.load_frames()
        self.load_data()

    def delete_room(self, room_number):
        num_of_reservations = self.db_driver.reserved_room_queries.get_num_of_reservations_from_room(room_number)
        num_of_bookings = self.db_driver.booked_room_queries.get_num_of_bookings_from_room(room_number)

        if num_of_reservations == 0 and num_of_bookings == 0:
            header_message = "Are you sure you want to delete this room?"
            subheader_message = "Double check all input fields before proceeding."
            self.confirmation_dialog = ConfirmationDialog(header_message, subheader_message)

            self.confirmation_dialog.exec()

            if self.confirmation_dialog.get_choice():
                self.db_driver.room_queries.soft_delete_room(room_number)

            self.success_dialog = FeedbackDialog(f"{room_number} deleted successfully.")
            self.success_dialog.exec()

            self.set_models()
            self.load_frames()
            self.load_data()

        else:

            if num_of_bookings == 0:
                subheader_message = f"It currently has a reservation."
            else:
                subheader_message = f"It currently has a booking."

            self.feedback_dialog = FeedbackDialog("Room can't be deleted.", subheader_message)

            self.feedback_dialog.exec()

    def connect_signals_to_slots(self):

        self.view.window_resized.connect(self.update_frame_count)

        self.view.change_view_mode.connect(self.change_view_mode)

        self.view.next_page_button_pressed.connect(self.go_to_next_page)

        self.view.previous_page_button_pressed.connect(self.go_to_previous_page)

        self.view.clicked_add_room_button.connect(lambda: self.open_add_edit_room_dialog("add_room"))

    def go_to_next_page(self):
        if self.rooms_model.set_next_page(self.view_mode):
            self.load_frames()
            self.load_data()

    def go_to_previous_page(self):
        if self.rooms_model.set_previous_page():
            self.load_frames()
            self.load_data()

    def change_view_mode(self, new_view_mode):

        if self.view_mode == new_view_mode:
            return

        if new_view_mode == "list_view":
            self.view_mode = "list_view"

            self.rooms_model.set_max_rows_per_page(self.view.get_list_view_current_max_rows())
            self.rooms_model.set_max_columns_per_page(-1)

        elif new_view_mode == "grid_view":
            self.view_mode = "grid_view"

            self.rooms_model.set_max_rows_per_page(self.view.get_grid_view_current_max_rows())
            self.rooms_model.set_max_columns_per_page(self.view.get_grid_view_current_max_columns())

        self.rooms_model.reset()

        self.load_frames()
        self.load_data()

    def update_frame_count(self, widget):

        if widget == self.view.list_view_widget:
            self.update_list_view_contents()

        elif widget == self.view.grid_view_widget:
            self.update_grid_view_contents()

    def update_list_view_contents(self):
        new_rows = self.view.get_list_view_current_max_rows()
        print(new_rows)

        if new_rows != self.rooms_model.get_max_rows_per_page():
            self.rooms_model.set_max_rows_per_page(new_rows)
            self.rooms_model.check_if_underflow_contents(self.view_mode)
            self.load_frames()
            self.load_data()

    def update_grid_view_contents(self):
        new_rows = self.view.get_grid_view_current_max_rows()
        new_columns = self.view.get_grid_view_current_max_columns()

        if (new_rows != self.rooms_model.get_max_rows_per_page()) or (new_columns != self.rooms_model.get_max_columns_per_page()):
            self.rooms_model.set_max_rows_per_page(new_rows)
            self.rooms_model.set_max_columns_per_page(new_columns)
            self.rooms_model.check_if_underflow_contents(self.view_mode)
            self.load_frames()
            self.load_data()
