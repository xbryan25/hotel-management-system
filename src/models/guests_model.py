from PyQt6.QtCore import QAbstractTableModel, Qt
from datetime import datetime


class GuestsModel(QAbstractTableModel):
    def __init__(self, _data=None):
        super().__init__()

        self.data = _data or []

        self.columns = ["Guest ID", "Guest Name", "Room No.", "Check In", "Check Out", "Room Type", "Amount Due", ""]

    def update_data(self, _data):
        self.beginResetModel()
        self.data = _data
        self.endResetModel()

    def get_guest_id(self, row):
        return self.data[row][0]

    def rowCount(self, index=None):
        return len(self.data)

    def columnCount(self, index=None):
        # -1 because Guest ID will be hidden
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:

            if index.column() == 2:
                value = self.data[index.row()][index.column()].replace("room-", "#")
            elif index.column() == 3 or index.column() == 4:
                value = self.data[index.row()][index.column()].strftime("%b %d, %Y %I:%M %p")
            elif index.column() == 6:
                value = "-"
            elif index.column() == 7:
                value = ""
            else:
                value = self.data[index.row()][index.column()]

            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
