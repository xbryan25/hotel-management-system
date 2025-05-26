from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor, QIcon

import sys
import ctypes

from views.application_window import ApplicationWindow


def main():

    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("hotel.ease")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon("../resources/icons/hms_db_icon"))

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#F1F1F1"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#F1F1F1"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#000000"))
    app.setPalette(palette)

    application_window = ApplicationWindow()
    application_window.show()

    app.exec()


if __name__ == "__main__":
    main()
