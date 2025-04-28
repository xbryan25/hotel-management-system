from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QApplication, QStyle
from PyQt6.QtCore import Qt, pyqtSignal, QModelIndex, QSize
from PyQt6.QtGui import QMouseEvent, QCursor, QIcon


class ButtonDelegate(QStyledItemDelegate):
    clicked = pyqtSignal(QModelIndex)  # Signal when button is clicked

    def __init__(self, parent=None):
        super().__init__(parent)

    # Load visual representation
    def paint(self, painter, option, index):

        button = QStyleOptionButton()
        button.rect = option.rect
        button.text = ""
        button.icon = QIcon("../resources/icons/guests_page/info_icon.svg")

        # button.iconSize = button.rect.size()

        button.iconSize = QSize(24, 24)

        # |= is bitwise operator OR
        button.features |= QStyleOptionButton.ButtonFeature.Flat
        button.state = QStyle.StateFlag.State_Enabled

        QApplication.style().drawControl(QStyle.ControlElement.CE_PushButton, button, painter)

        super().paint(painter, option, index)

    # Handle events made to the button
    def editorEvent(self, event, model, option, index):
        button_rect = option.rect

        if button_rect.contains(event.pos()):
            if event.type() == QMouseEvent.Type.MouseButtonRelease:
                if button_rect.contains(event.pos()):
                    self.clicked.emit(index)
                    return True

        return False
