from PyQt6.QtCore import QAbstractTableModel, Qt
from datetime import datetime


class BookingModel(QAbstractTableModel):
    BUTTON_ENABLED_ROLE = Qt.ItemDataRole.UserRole + 1

    def __init__(self, data=None):
        super().__init__()

        self._data = data or []

        self.columns = ["Booking ID", "Guest Name", "Room No.", "Room Type", "Check-in & Check-out", "", ""]

    def update_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:

            if index.column() == 4:
                check_in_date = self._data[index.row()][index.column()]
                check_out_date = self._data[index.row()][index.column() + 1]

                if isinstance(check_in_date, datetime) and isinstance(check_out_date, datetime):
                    return f"{check_in_date.strftime("%b %d, %Y")} - {check_out_date.strftime("%b %d, %Y")}"

                return None

            elif index.column() in [5, 6]:
                return ""

            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.ToolTipRole:
            if index.column() == 6:
                return "View booking details?"
            elif index.column() == 7:
                return "Check out?"

        if role == self.BUTTON_ENABLED_ROLE and index.column() == 6:
            check_in_status = self._data[index.row()][6]  # assume column 1 holds status

            return check_in_status == "in progress"

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
