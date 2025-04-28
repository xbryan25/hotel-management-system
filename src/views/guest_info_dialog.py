from PyQt6.QtWidgets import QDialog

from ui.guest_info_dialog_ui import Ui_Dialog as GuestInfoDialogUI


class GuestInfoDialog(QDialog, GuestInfoDialogUI):
    def __init__(self):

        super().__init__()

        self.setupUi(self)

        self.connect_signals_to_slots()

    def connect_signals_to_slots(self):
        self.edit_guest_button.clicked.connect(lambda: self.information_stacked_widget.setCurrentWidget(self.edit_mode_widget))
