from PyQt6.QtCore import QAbstractTableModel, Qt


class RoomsModel(QAbstractTableModel):
    def __init__(self, room_list: list[dict], model_type='rooms_page'):
        super().__init__()

        self._rooms = room_list

        self.model_type = model_type

        if self.model_type == 'rooms_page':
            self.columns = ["Room No.", "Status"]
        elif self.model_type == 'nrd_room_numbers':
            self.columns = ["Room No."]
        else:
            self.columns = ["Room Types"]

        # nrd = new_reservation_dialog
        if self.model_type == 'nrd_room_types' and self._rooms:
            self.convert_rooms_with_unique_room_types()

    def get_cost_of_room(self, room_number):
        for room in self._rooms:
            if room[0] == room_number:
                return room[2]

    def convert_rooms_with_unique_room_types(self):
        unique_rooms = []

        seen = set()

        for room in self._rooms:
            value = room[1]
            if value not in seen:
                unique_rooms.append(room)
                seen.add(value)


        unique_rooms.insert(0, [None, "-"])

        self._rooms = unique_rooms

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
            if self.model_type == 'nrd_room_numbers' and index.column() == 0:
                return self._rooms[index.row()][0]
            elif self.model_type == 'nrd_room_types' and index.column() == 0:
                return self._rooms[index.row()][1]
            elif self.model_type == 'rooms_page' and index.column() == 0:
                return self._rooms[index.row()][0]
            elif self.model_type == 'rooms_page' and index.column() == 1:
                return self._rooms[index.row()][3]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
