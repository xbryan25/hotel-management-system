from PyQt6.QtWidgets import QMainWindow

from application.application_window_design import Ui_MainWindow as ApplicationWindowDesign
from database_driver.database_driver import DatabaseDriver


class ApplicationWindow(QMainWindow, ApplicationWindowDesign):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.db_driver = DatabaseDriver()


