from PyQt6.QtCore import QAbstractTableModel, Qt
from datetime import datetime


class RecentStaysModel(QAbstractTableModel):
    def __init__(self, _data=None):
        super().__init__()

        # self.data = _data

        self.data = _data or []

        self.columns = ["Booking ID", "Guest Name", "Room No.", "Time"]

    def update_data(self, _data):
        self.beginResetModel()
        self.data = _data
        self.endResetModel()

    def rowCount(self, index=None):
        return len(self.data)

    def columnCount(self, index=None):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            value = self.data[index.row()][index.column()]

            if isinstance(value, datetime):
                return value.strftime("%I:%M %p")

            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.ToolTipRole:
            if index.column() == 1:
                return self.data[index.row()][1]

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
