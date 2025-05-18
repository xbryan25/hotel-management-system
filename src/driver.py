from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
import sys

from views.application_window import ApplicationWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

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
