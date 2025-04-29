from PyQt6.QtCore import QAbstractListModel, Qt


class AvailableRoomsModel(QAbstractListModel):
    def __init__(self, rooms):
        super().__init__()
        self._rooms = rooms

    def rowCount(self, parent=None):
        return len(self._rooms)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._rooms[index.row()]

    def set_rooms(self, rooms):
        self.beginResetModel()
        self._rooms = rooms
        self.endResetModel()
