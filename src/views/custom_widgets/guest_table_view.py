from PyQt6.QtWidgets import QTableView, QApplication
from PyQt6.QtCore import Qt


class CustomTableView(QTableView):
    def __init__(self, parent, table_view_mode=None):

        super().__init__(parent)

        self.setShowGrid(False)
        self.setMouseTracking(True)
        self.setObjectName(f"{table_view_mode}_table_view")
        self.verticalHeader().setVisible(False)

        self._hovered = False

    def hide_first_column(self):
        # Hide 'Guest ID' column
        self.setColumnHidden(0, True)

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
