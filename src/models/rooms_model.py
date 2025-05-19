from PyQt6.QtCore import QAbstractTableModel, Qt


class RoomsModel(QAbstractTableModel):
    def __init__(self, room_list: list[dict], initial_rows_per_page=None, initial_columns_per_page=None):
        super().__init__()

        self._rooms = room_list

        self.columns = ["Room No.", "Status"]

    def get_contents(self):
        return self._rooms

    def get_len_of_data(self):
        return len(self._rooms)

    def update_data(self, rooms):
        self.beginResetModel()
        self._rooms = rooms
        self.endResetModel()

    # Only for dashboard
    def rowCount(self, index=None):
        return self.get_len_of_data()

    def columnCount(self, index=None):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return self._rooms[index.row()][0]

            elif index.column() == 1:
                return self._rooms[index.row()][3]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
