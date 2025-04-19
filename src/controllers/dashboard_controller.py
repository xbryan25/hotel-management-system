

class DashboardController:
    def __init__(self, page_widget, db_driver):
        self.view = page_widget
        self.db_driver = db_driver
