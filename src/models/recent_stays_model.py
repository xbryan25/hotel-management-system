from PyQt6.QtCore import QAbstractTableModel, Qt


class RecentStaysModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()

        # self.data = _data

        self.temp_data = [["", "", "", ""]]

        self.columns = ["Booking ID", "Guest Name", "Room No.", "Time"]

    def rowCount(self, index=None):
        return len(self.temp_data)

    def columnCount(self, index=None):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self.temp_data[index.row()][index.column()]

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
