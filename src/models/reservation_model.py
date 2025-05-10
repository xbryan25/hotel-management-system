from PyQt6.QtCore import QAbstractTableModel, Qt
from datetime import datetime


class ReservationModel(QAbstractTableModel):
    def __init__(self, _data=None, view_mode="dashboard_view"):
        super().__init__()

        self.data = _data or []

        if view_mode == "dashboard_view":
            self.columns = ["Reservation ID", "Guest Name", "Room No.", "Room Type", "Check-in & Check-out", "Status"]
        else:
            self.columns = ["Reservation ID", "Guest Name", "Room No.", "Room Type", "Check-in & Check-out", "Status", "", ""]

    def update_data(self, _data):
        self.beginResetModel()
        self.data = _data
        self.endResetModel()

    def rowCount(self, index=None):
        return len(self.data)

    def columnCount(self, index=None):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:

            if index.column() == 4:
                check_in_date = self.data[index.row()][index.column()]
                check_out_date = self.data[index.row()][index.column() + 1]

                if isinstance(check_in_date, datetime) and isinstance(check_out_date, datetime):
                    return f"{check_in_date.strftime("%b %d, %Y")} - {check_out_date.strftime("%b %d, %Y")}"

                return None

            elif index.column() == 5:
                return self.data[index.row()][index.column() + 1]

            elif index.column() == 6 or index.column() == 7:
                return ""

            return self.data[index.row()][index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.ToolTipRole:
            if index.column() == 6:
                return "View reservation details?"
            elif index.column() == 7:
                return "Check in?"

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
