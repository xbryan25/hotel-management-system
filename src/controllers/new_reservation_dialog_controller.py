from models.available_rooms_model import AvailableRoomsModel


class NewReservationDialogController:
    def __init__(self, dialog, db_driver):
        self.view = dialog
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.set_models()

    def connect_signals_to_slots(self):
        self.view.room_type_changed.connect(self.update_models)

    def set_models(self):
        available_rooms = self.db_driver.get_available_rooms()

        # list(available_rooms) makes a copy of available_rooms so that it won't be affected
        self.available_room_numbers_model = AvailableRoomsModel(available_rooms, 0)
        self.available_room_types_model = AvailableRoomsModel(list(available_rooms), 1)

        self.view.rooms_combobox.setModel(self.available_room_numbers_model)

        self.view.room_type_filter_combobox.blockSignals(True)
        self.view.room_type_filter_combobox.setModel(self.available_room_types_model)
        self.view.room_type_filter_combobox.blockSignals(False)

    def update_models(self, room_type):

        if room_type == "-":
            available_rooms_from_room_type = self.db_driver.get_available_rooms()
        else:
            available_rooms_from_room_type = self.db_driver.get_available_rooms(room_type)

        self.available_room_numbers_model.set_rooms(available_rooms_from_room_type)
