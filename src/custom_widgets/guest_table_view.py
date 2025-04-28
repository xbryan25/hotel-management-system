from PyQt6.QtWidgets import QTableView, QApplication
from PyQt6.QtCore import Qt

class GuestTableView(QTableView):
    def __init__(self, parent):

        super().__init__(parent)

        self.setShowGrid(False)
        self.setMouseTracking(True)
        self.setObjectName("guest_table_view")
        self.verticalHeader().setVisible(False)

        self._hovered = False

    def mouseMoveEvent(self, event):

        index = self.indexAt(event.pos())

        column = index.column()
        last_column = self.model().columnCount() - 1

        if column == last_column:
            if not self._hovered:
                QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
                self._hovered = True

        else:
            if self._hovered:
                QApplication.restoreOverrideCursor()
                self._hovered = False

        super().mouseMoveEvent(event)

    def leaveEvent(self, event):

        if self._hovered:
            QApplication.restoreOverrideCursor()
            self._hovered = False

        super().leaveEvent(event)
