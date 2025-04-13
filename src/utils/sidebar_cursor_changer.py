from PyQt6.QtCore import Qt, QObject, QEvent


# Checks if the item that the mouse is currently hovering is an item in the list widget
# If so, the cursor changes to pointing hand cursor

class SidebarCursorChanger(QObject):
    def __init__(self, list_widget):

        super().__init__(list_widget)
        self.list_widget = list_widget

    def eventFilter(self, obj, event):

        if event.type() == QEvent.Type.MouseMove:
            item = self.list_widget.itemAt(event.position().toPoint())

            if item:
                self.list_widget.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                self.list_widget.setCursor(Qt.CursorShape.ArrowCursor)

        elif event.type() == QEvent.Type.Leave:
            self.list_widget.setCursor(Qt.CursorShape.ArrowCursor)

        return super().eventFilter(obj, event)
