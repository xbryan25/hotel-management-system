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
        self.table_view_mode = table_view_mode

        self.horizontalHeader().setMinimumSectionSize(25)

    def hide_first_column(self):
        # Hide 'Guest ID' column
        self.setColumnHidden(0, True)

    def mouseMoveEvent(self, event):

        index = self.indexAt(event.pos())

        column = index.column()
        last_column = self.model().columnCount() - 1

        if index.isValid():
            delegate = self.itemDelegateForColumn(index.column())

            if hasattr(delegate, "enable_role") and delegate.enable_role and delegate.can_be_disabled:
                enabled = index.model().data(index, delegate.enable_role)
                if not enabled:
                    if self._hovered:
                        QApplication.restoreOverrideCursor()
                        self._hovered = False

                    self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
                    super().mouseMoveEvent(event)
                    return

        if self.table_view_mode in ("guests", "billings"):
            if column == last_column:
                if not self._hovered:
                    QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
                    self._hovered = True

            else:
                if self._hovered:
                    QApplication.restoreOverrideCursor()
                    self._hovered = False

        elif self.table_view_mode in ("reservations", "bookings"):
            second_last_column = self.model().columnCount() - 2

            if column == last_column or column == second_last_column:
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
