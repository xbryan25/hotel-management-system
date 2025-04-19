from PyQt6.QtWidgets import QWidget

from ui.billing_page_ui import Ui_Widget as BillingPageUI


class BillingPage(QWidget, BillingPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
