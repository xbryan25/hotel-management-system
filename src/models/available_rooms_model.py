from PyQt6.QtCore import QAbstractListModel, Qt


class AvailableRoomsModel(QAbstractListModel):
    def __init__(self, rooms, field_index):
        super().__init__()
        self._rooms = rooms
        self._field_index = field_index

        if self._field_index == 1:
            unique_rooms = []

            seen = set()

            for room in self._rooms:
                value = room[self._field_index]
                if value not in seen:
                    unique_rooms.append(room)
                    seen.add(value)

            unique_rooms.insert(0, [None, "-"])

            self._rooms = unique_rooms

    def get_cost_of_room(self, room_number):
        for room in self._rooms:
            if room[0] == room_number:
                return room[2]



    def rowCount(self, parent=None):
        return len(self._rooms)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:

            return self._rooms[index.row()][self._field_index]

    def set_rooms(self, rooms):
        self.beginResetModel()
        self._rooms = rooms
        self.endResetModel()
