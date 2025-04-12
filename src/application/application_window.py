from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt

from application.application_window_design import Ui_MainWindow as ApplicationWindowDesign
from database_driver.database_driver import DatabaseDriver


class ApplicationWindow(QMainWindow, ApplicationWindowDesign):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.db_driver = DatabaseDriver()

        self.collapsed_sidebar_frame.setVisible(False)

        self.show_icons_only_button.clicked.connect(self.show_collapsed_sidebar_frame)
        self.show_icons_and_text_button.clicked.connect(self.show_expanded_sidebar_frame)

        self.collapsed_buttons_list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.expanded_buttons_list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.set_external_stylesheet()
        self.add_signals_to_sidebar_items()

    def show_collapsed_sidebar_frame(self):
        self.collapsed_sidebar_frame.setVisible(True)
        self.expanded_sidebar_frame.setVisible(False)

    def show_expanded_sidebar_frame(self):
        self.collapsed_sidebar_frame.setVisible(False)
        self.expanded_sidebar_frame.setVisible(True)

    def add_signals_to_sidebar_items(self):
        # Connects the index of the list widget to the index of the stacked widget
        self.expanded_buttons_list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.collapsed_buttons_list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # Connects the expanded buttons list widget to the collapsed buttons list widget and vice versa
        self.expanded_buttons_list_widget.currentRowChanged.connect(self.collapsed_buttons_list_widget.setCurrentRow)
        self.collapsed_buttons_list_widget.currentRowChanged.connect(self.expanded_buttons_list_widget.setCurrentRow)

    def set_external_stylesheet(self):
        with open("../resources/styles/sidebar.qss", "r") as file:
            self.sidebar_frame.setStyleSheet(file.read())
