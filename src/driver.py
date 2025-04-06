from PyQt6.QtWidgets import QApplication

from application.application_window import ApplicationWindow


def main():

    app = QApplication([])

    application_window = ApplicationWindow()

    application_window.show()
    app.exec()


if __name__ == "__main__":
    main()
