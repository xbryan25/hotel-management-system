from PyQt6.QtCore import QTimer

from models import RoomsModel
from views import AddRoomDialog
from controllers.add_room_dialog_controller import AddRoomDialogController


class RoomsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.view_mode = "list_view"

        self.set_models()

        self.connect_signals_to_slots()

        self.load_frames()
        self.load_data()

    def set_models(self):
        rooms_initial_data = self.db_driver.room_queries.get_all_rooms()

        # Only for list view
        initial_rows = self.view.get_list_view_current_max_rows()

        self.rooms_model = RoomsModel(rooms_initial_data, initial_rows, -1)

    def load_frames(self):
        if self.view_mode == "list_view":
            self.view.make_list_view_rooms_frame(self.rooms_model.get_per_page(self.view_mode))
        else:
            self.view.make_grid_view_rooms_frame(self.rooms_model.get_per_page(self.view_mode))

    def load_data(self):
        if self.view_mode == "list_view":
            self.view.update_list_view_frames_contents(self.rooms_model.get_rooms_from_current_page(self.view_mode))
        else:
            self.view.update_grid_view_frames_contents(self.rooms_model.get_rooms_from_current_page(self.view_mode))

    def open_add_room_dialog(self):
        self.add_room_dialog = AddRoomDialog()
        self.add_room_dialog_controller = AddRoomDialogController(self.add_room_dialog, self.db_driver)

        self.add_room_dialog.exec()

    def connect_signals_to_slots(self):

        self.view.window_resized.connect(self.update_frame_count)

        self.view.change_view_mode.connect(self.change_view_mode)

        self.view.next_page_button_pressed.connect(self.go_to_next_page)

        self.view.previous_page_button_pressed.connect(self.go_to_previous_page)

        self.view.clicked_add_room_button.connect(self.open_add_room_dialog)

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
