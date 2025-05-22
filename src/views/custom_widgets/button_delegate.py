from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QApplication, QStyle
from PyQt6.QtCore import Qt, pyqtSignal, QModelIndex, QSize
from PyQt6.QtGui import QMouseEvent, QCursor, QIcon, QColor, QBrush


class ButtonDelegate(QStyledItemDelegate):
    clicked = pyqtSignal(QModelIndex)  # Signal when button is clicked

    def __init__(self, icon_path, can_be_disabled, parent=None, alt_icon_path=None):
        super().__init__(parent)

        self.icon_path = icon_path
        self.can_be_disabled = can_be_disabled
        self.enable_role = Qt.ItemDataRole.UserRole + 1
        self.alt_icon_path = alt_icon_path

    # Load visual representation
    def paint(self, painter, option, index):

        painter.save()
        painter.fillRect(option.rect, QBrush(QColor("#FFFFFF")))  # Light blue, for example
        painter.restore()

        button = QStyleOptionButton()
        button.rect = option.rect
        button.text = ""
        button.icon = QIcon(self.icon_path)

        # Only for ServicesModel restore feature
        if index.model().__class__.__name__ == "ServicesModel":
            if index.column() == 4 and index.model().get_active_status_of_service(index.row()) == 0:
                button.icon = QIcon(self.alt_icon_path)

        # button.iconSize = button.rect.size()

        button.iconSize = QSize(24, 24)

        # |= is bitwise operator OR
        button.features |= QStyleOptionButton.ButtonFeature.Flat
        button.state = QStyle.StateFlag.State_Enabled

        if self.can_be_disabled:
            enabled = index.model().data(index, self.enable_role)

            # If disabled, then don't draw the button at all
            if not enabled:
                return

        QApplication.style().drawControl(QStyle.ControlElement.CE_PushButton, button, painter)

        # super().paint(painter, option, index)

    # Handle events made to the button
    def editorEvent(self, event, model, option, index):
        if self.can_be_disabled:
            enabled = index.model().data(index, self.enable_role)

            # If disabled, then don't accept click events
            if not enabled:
                return False

        button_rect = option.rect

        if button_rect.contains(event.pos()):
            if event.type() == QMouseEvent.Type.MouseButtonRelease:
                if button_rect.contains(event.pos()):
                    self.clicked.emit(index)
                    return True

        return False

    def sizeHint(self, option, index):
        return QSize(25, option.rect.height())
