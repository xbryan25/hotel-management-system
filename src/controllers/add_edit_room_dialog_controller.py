
from PyQt6.QtWidgets import QFileDialog
import shutil
import os

from views import FeedbackDialog
from models import AvailableRoomsModel


class AddEditRoomDialogController:
    def __init__(self, dialog, db_driver, dialog_type, room_number):
        self.view = dialog
        self.db_driver = db_driver

        self.dialog_type = dialog_type
        self.room_number = room_number
        self.image_file_path = None

        self.set_models()

        self.connect_signals_to_slots()

        self.load_details_from_dialog_type()

    def load_details_from_dialog_type(self):
        if self.dialog_type == "edit_room":

            room_details = self.db_driver.room_queries.get_room_details(self.room_number)

            self.view.load_edit_room_view(self.room_number, room_details)

            filename = self.db_driver.room_queries.get_room_image(self.room_number)
            self.image_file_path = "../resources/icons/rooms_page/room_images/" + filename

            self.view.update_chosen_image_label(filename)

    def connect_signals_to_slots(self):
        self.view.clicked_add_edit_room_button.connect(self.add_or_edit_room)
        self.view.clicked_browse_image_button.connect(self.choose_image)

    def choose_image(self):
        self.image_file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Open Image File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        filename = os.path.basename(self.image_file_path)

        self.view.update_chosen_image_label(filename)

    def set_models(self):
        all_rooms = self.db_driver.room_queries.get_all_rooms()

        # TODO: Change model? It's not really only available rooms
        self.available_room_numbers_model = AvailableRoomsModel(all_rooms, 1, model_type="rooms")
        self.view.room_type_value_combobox.setModel(self.available_room_numbers_model)

    def add_or_edit_room(self, room_number):

        if self.db_driver.room_queries.check_if_room_number_exists(room_number) and self.room_number != room_number:
            self.feedback_dialog = FeedbackDialog(f"{room_number} already exists. Try again.")
            self.feedback_dialog.exec()
            return

        room_detail_inputs = self.view.get_room_detail_inputs()

        # Create target directory if it doesn't exist
        room_images_dir = "../resources/icons/rooms_page/room_images"
        target_dir = os.path.join(os.getcwd(), room_images_dir)
        os.makedirs(target_dir, exist_ok=True)

        filename = os.path.basename(self.image_file_path)
        dest_path = os.path.join(target_dir, filename)

        # Check if they both lead to the same file
        if os.path.abspath(os.path.normpath(self.image_file_path)) != os.path.abspath(os.path.normpath(dest_path)):
            # Copy the file
            shutil.copy(self.image_file_path, dest_path)

        room_detail_inputs.update({'image_file_name': filename})

        if self.dialog_type == "add_room":
            self.db_driver.room_queries.add_room(room_detail_inputs)

            header_message = "Room added successfully."
        else:
            # room_detail_inputs.update({'image_file_name': filename})
            self.db_driver.room_queries.update_room(self.room_number, room_detail_inputs)

            header_message = "Room edited successfully."


        self.success_dialog = FeedbackDialog(header_message, connected_view=self.view)
        self.success_dialog.exec()
