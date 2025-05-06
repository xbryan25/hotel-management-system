from PyQt6.QtWidgets import QWidget

from ui import BillingPageUI


class BillingPage(QWidget, BillingPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
