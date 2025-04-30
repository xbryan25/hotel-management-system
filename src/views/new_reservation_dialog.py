from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import pyqtSignal

from ui.new_reservation_dialog_ui import Ui_Dialog as NewReservationDialogUI


class NewReservationDialog(QDialog, NewReservationDialogUI):
    room_type_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_signals_to_slots()

        self.current_page = 1

    def connect_signals_to_slots(self):
        self.left_button.clicked.connect(lambda: self.page_change("left_button"))
        self.right_button.clicked.connect(lambda: self.page_change("right_button"))

        self.room_type_filter_combobox.currentTextChanged.connect(self.room_type_changed.emit)

    def page_change(self, button_type):
        if self.current_page < 3 and button_type == "right_button":
            self.current_page += 1
        elif self.current_page >= 1 and button_type == "left_button":
            self.current_page -= 1

        # print(self.current_page)

        self.contents_stacked_widget.setCurrentIndex(self.current_page - 1)
