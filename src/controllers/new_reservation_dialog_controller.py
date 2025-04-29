from models.available_rooms_model import AvailableRoomsModel


class NewReservationDialogController:
    def __init__(self, dialog, db_driver):
        self.view = dialog
        self.db_driver = db_driver

    def set_models(self):
        available_rooms = self.db_driver.get_available_rooms()

        self.available_rooms_model = AvailableRoomsModel(available_rooms)

        self.view.rooms_combobox.setModel(self.guests_model)
