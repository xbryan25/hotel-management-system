from PyQt6.QtCore import QAbstractTableModel, Qt
from datetime import datetime


class GuestsModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()

        self._data = data or []

        self.columns = ["Guest ID", "Guest Name", "Phone Number", "Last Visit Date", "Visit Count", "Total Amount Due", ""]

    def update_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

        self.layoutChanged.emit()

    def get_guest_id(self, row):
        return self._data[row][0]

    def get_len_of_data(self):
        return len(self._data)

    def get_data(self):
        return self._data

    def rowCount(self, index=None):
        return self.get_len_of_data()

    def columnCount(self, index=None):
        # -1 because Guest ID will be hidden
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:

            if index.column() == 3 and self._data[index.row()][index.column()]:
                value = self._data[index.row()][index.column()].strftime("%b %d, %Y")
            elif index.column() == 3 and not self._data[index.row()][index.column()]:
                value = "-"
            elif index.column() == 5:
                value = self._data[index.row()][index.column()]
            elif index.column() == 6:
                value = ""
            else:
                value = self._data[index.row()][index.column()]

            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
