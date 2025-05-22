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

        self.connect_signals_to_slots()

        self.is_load_contents = False

        self.prev_sort_by = None
        self.prev_sort_type = None
        self.prev_search_input = None

        self.current_page = 1
        self.max_rows_per_page = 5
        self.max_columns_per_page = 2

    def set_models(self, max_room_per_page=5, current_page_number=1,
                   sort_by="room_number", sort_type="ASC", search_input=None):

        rooms_data = self.db_driver.room_queries.get_all_rooms(enable_pagination=True,
                                                               max_room_per_page=max_room_per_page,
                                                               current_page_number=current_page_number,
                                                               sort_by=sort_by,
                                                               sort_type=sort_type,
                                                               search_input=search_input)

        # Only for list view
        initial_rows = self.view.get_list_view_current_max_rows()

        if not self.rooms_model:
            self.rooms_model = RoomsModel(rooms_data)
        else:
            self.rooms_model.update_data(rooms_data)

    def load_frames(self):
        if self.view_mode == "list_view":
            self.view.make_list_view_rooms_frame(self.rooms_model.get_len_of_data())
        else:
            self.view.make_grid_view_rooms_frame(self.rooms_model.get_len_of_data())

    def load_data(self):

        if self.view_mode == "list_view":
            self.view.update_list_view_frames_contents(self.rooms_model.get_contents(),
                                                       self.open_add_edit_room_dialog, self.delete_room)
        else:
            self.view.update_grid_view_frames_contents(self.rooms_model.get_contents(),
                                                       self.open_add_edit_room_dialog, self.delete_room)

    def open_add_edit_room_dialog(self, dialog_type, room_number=None):
        self.add_edit_room_dialog = AddEditRoomDialog()
        self.add_edit_room_dialog_controller = AddEditRoomDialogController(self.add_edit_room_dialog, self.db_driver,
                                                                           dialog_type, room_number)

        self.add_edit_room_dialog.exec()

        self.refresh_rooms_data()

    def delete_room(self, room_number):
        num_of_reservations = self.db_driver.reserved_room_queries.get_num_of_reservations_from_room(room_number)
        num_of_bookings = self.db_driver.booked_room_queries.get_num_of_bookings_from_room(room_number)

        if num_of_reservations == 0 and num_of_bookings == 0:
            header_message = "Are you sure you want to delete this room?"
            subheader_message = "Connected reservations and bookings will also be removed."
            self.confirmation_dialog = ConfirmationDialog(header_message, subheader_message)

            self.confirmation_dialog.exec()

            if self.confirmation_dialog.get_choice():
                self.db_driver.room_queries.delete_room(room_number)

                self.refresh_rooms_data()

                self.success_dialog = FeedbackDialog(f"{room_number} deleted successfully.")
                self.success_dialog.exec()

        else:

            if num_of_bookings == 0:
                subheader_message = f"It currently has a reservation."
            else:
                subheader_message = f"It currently has a booking."

            self.feedback_dialog = FeedbackDialog("Room can't be deleted.", subheader_message)

            self.feedback_dialog.exec()

    def connect_signals_to_slots(self):

        self.view.sort_by_combobox.currentTextChanged.connect(self.refresh_rooms_data)
        self.view.sort_type_combobox.currentTextChanged.connect(self.refresh_rooms_data)

        self.view.window_resized.connect(self.update_frame_count)

        self.view.change_view_mode.connect(self.change_view_mode)

        self.view.next_page_button_pressed.connect(self.go_to_next_page)

        self.view.previous_page_button_pressed.connect(self.go_to_previous_page)

        self.view.clicked_add_room_button.connect(lambda: self.open_add_edit_room_dialog("add_room"))

        self.view.search_text_changed.connect(self.update_prev_search_input)
        self.view.search_text_changed.connect(lambda _: self.refresh_rooms_data())

    def update_prev_search_input(self, search_input):
        self.prev_search_input = search_input

    def go_to_next_page(self):
        room_count = self.db_driver.room_queries.get_room_count("all", search_input=self.prev_search_input)

        if self.current_page + 1 <= self.total_pages(room_count):
            self.current_page += 1

            self.refresh_rooms_data()
            # print()
            # print(self.rooms_model.get_len_of_data())
            # print(self.rooms_model.get_contents())

    def go_to_previous_page(self):

        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_rooms_data()

    def total_pages(self, room_count):

        if self.view_mode == "list_view":
            return (room_count + self.max_rows_per_page - 1) // self.max_rows_per_page
        else:
            return ((room_count - 1) // (self.max_rows_per_page * self.max_columns_per_page)) + 1

    def change_view_mode(self, new_view_mode):

        self.current_page = 1

        if self.view_mode == new_view_mode:
            return

        if new_view_mode == "list_view":
            self.view_mode = "list_view"

            self.max_rows_per_page = self.view.get_list_view_current_max_rows()
            self.max_columns_per_page = -1

        elif new_view_mode == "grid_view":
            self.view_mode = "grid_view"

            self.max_rows_per_page = self.view.get_grid_view_current_max_rows()
            self.max_columns_per_page = self.view.get_grid_view_current_max_columns()

        self.refresh_rooms_data()

    def refresh_rooms_data(self):

        self.prev_sort_by = self.view.sort_by_combobox.currentText().replace("Sort by ", "").lower().replace(" ", "_")
        self.prev_sort_type = "ASC" if self.view.sort_type_combobox.currentText() == "Ascending" else "DESC"

        if self.view_mode == "list_view":
            self.set_models(max_room_per_page=self.max_rows_per_page,
                            current_page_number=self.current_page,
                            sort_by=self.prev_sort_by,
                            sort_type=self.prev_sort_type,
                            search_input=self.prev_search_input)
        else:
            self.set_models(max_room_per_page=self.max_rows_per_page * self.max_columns_per_page,
                            current_page_number=self.current_page,
                            sort_by=self.prev_sort_by,
                            sort_type=self.prev_sort_type,
                            search_input=self.prev_search_input)

        if self.check_if_underflow_contents():
            # return because this is a recursive call, frames are already loaded in self.current_page - 1
            return
        else:
            self.load_frames()
            self.load_data()

    def check_if_underflow_contents(self):
        if self.rooms_model.get_len_of_data() == 0:
            self.go_to_previous_page()
            return True

        return False

    def update_frame_count(self):

        if self.view_mode == "list_view":
            self.update_list_view_contents()

        elif self.view_mode == "grid_view":
            self.update_grid_view_contents()

    def update_list_view_contents(self):
        new_rows = self.view.get_list_view_current_max_rows()

        if new_rows != self.max_rows_per_page:
            self.max_rows_per_page = new_rows

            self.refresh_rooms_data()

    def update_grid_view_contents(self):
        new_rows = self.view.get_grid_view_current_max_rows()
        new_columns = self.view.get_grid_view_current_max_columns()

        if (new_rows != self.max_rows_per_page) or (new_columns != self.max_columns_per_page):
            self.max_rows_per_page = new_rows
            self.max_columns_per_page = new_columns

            self.refresh_rooms_data()
