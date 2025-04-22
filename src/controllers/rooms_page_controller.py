from PyQt6.QtCore import QTimer

from models.rooms_model import RoomsModel


class RoomsPageController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver

        self.set_models()

        self.load_frames()
        self.load_data()
        self.connect_signals_to_slots()

    def set_models(self):
        rooms_initial_data = self.db_driver.get_all_rooms()

        initial_rows = self.view.get_list_view_current_max_rows()

        self.rooms_model = RoomsModel(rooms_initial_data, initial_rows)

    def load_frames(self):
        self.view.make_list_view_rooms_frame(self.rooms_model.get_per_page())

    def load_data(self):
        self.view.update_list_view_frames_contents(self.rooms_model.get_rooms_from_current_page())

    def connect_signals_to_slots(self):

        self.view.window_resized.connect(self.update_frame_count)

        self.view.next_page_button_pressed.connect(self.rooms_model.set_next_page)
        self.view.next_page_button_pressed.connect(self.load_frames)
        self.view.next_page_button_pressed.connect(self.load_data)

        self.view.previous_page_button_pressed.connect(self.rooms_model.set_previous_page)
        self.view.previous_page_button_pressed.connect(self.load_frames)
        self.view.previous_page_button_pressed.connect(self.load_data)

    def update_frame_count(self, widget):

        if widget == self.view.list_view_widget:
            self.update_list_view_rows()

        elif widget == self.view.grid_view_widget:
            print("Currently at grid view widget")

    def update_list_view_rows(self):
        new_rows = self.view.get_list_view_current_max_rows()
        print(new_rows)

        if new_rows != self.rooms_model.get_max_rows_per_page():
            self.rooms_model.set_max_rows_per_page(new_rows)
            self.load_frames()
            self.load_data()
