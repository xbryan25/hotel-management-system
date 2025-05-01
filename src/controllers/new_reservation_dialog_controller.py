from models.available_rooms_model import AvailableRoomsModel
from models.services_model import ServicesModel


class NewReservationDialogController:
    def __init__(self, dialog, db_driver):
        self.view = dialog
        self.db_driver = db_driver

        self.connect_signals_to_slots()

        self.set_models()

        self.view.load_services_frames(self.services_model.get_all())

    def connect_signals_to_slots(self):
        self.view.room_type_changed.connect(self.update_models)

        self.view.room_changed.connect(self.calculate_room_cost)
        self.view.date_time_changed.connect(self.calculate_room_cost)

    def calculate_room_cost(self, current_room):
        check_in_check_out_date_time = self.view.get_check_in_check_out_date_and_time()

        seconds = check_in_check_out_date_time["check_in"].secsTo(check_in_check_out_date_time["check_out"])

        hours = seconds / 3600

        current_room_cost = self.available_room_numbers_model.get_cost_of_room(current_room)

        total_room_cost = (((hours-1)//24) + 1) * current_room_cost

        self.view.update_room_cost_value_label(total_room_cost)

    # def calculate_total_service_cost(self, ):

    def set_models(self):
        available_rooms = self.db_driver.get_available_rooms()

        # list(available_rooms) makes a copy of available_rooms so that it won't be affected
        self.available_room_numbers_model = AvailableRoomsModel(available_rooms, 0)
        self.available_room_types_model = AvailableRoomsModel(list(available_rooms), 1)

        self.view.rooms_combobox.setModel(self.available_room_numbers_model)

        self.view.room_type_filter_combobox.blockSignals(True)
        self.view.room_type_filter_combobox.setModel(self.available_room_types_model)
        self.view.room_type_filter_combobox.blockSignals(False)

        available_services = self.db_driver.get_all_services()
        self.services_model = ServicesModel(available_services)


    def update_models(self, room_type):

        if room_type == "-":
            available_rooms_from_room_type = self.db_driver.get_available_rooms()
        else:
            available_rooms_from_room_type = self.db_driver.get_available_rooms(room_type)

        self.available_room_numbers_model.set_rooms(available_rooms_from_room_type)
