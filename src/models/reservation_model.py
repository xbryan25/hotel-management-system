from PyQt6.QtCore import QAbstractTableModel, Qt
from datetime import datetime


class ReservationModel(QAbstractTableModel):
    BUTTON_ENABLED_ROLE = Qt.ItemDataRole.UserRole + 1

    def __init__(self, data=None, view_mode="dashboard_view"):
        super().__init__()

        self._data = data or []

        self.view_mode = view_mode

        if self.view_mode == "dashboard_view":
            self.columns = ["Reservation ID", "Guest Name", "Room No.", "Room Type", "Check-in & Check-out", "Status"]
        elif self.view_mode == "billing_page_view":
            self.columns = ["Reservation ID", "Guest Name", "Room No.", "Total Reservation Cost", "Balance", ""]
        else:
            self.columns = ["Reservation ID", "Guest Name", "Room No.", "Room Type", "Check-in & Check-out", "Status", "", ""]

    def update_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

        self.layoutChanged.emit()

    def get_reservation_id(self, row):
        return self._data[row][0]

    def get_len_of_data(self):
        return len(self._data)

    def get_all(self):
        return self._data

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:

            if self.view_mode == "billing_page_view":

                if index.column() == 2 and not self._data[index.row()][index.column()]:
                    return "[deleted]"

                elif index.column() == 5:
                    return None

                return self._data[index.row()][index.column()]

            else:
                if index.column() == 4:
                    check_in_date = self._data[index.row()][index.column()]
                    check_out_date = self._data[index.row()][index.column() + 1]

                    if isinstance(check_in_date, datetime) and isinstance(check_out_date, datetime):
                        return f"{check_in_date.strftime("%b %d, %Y")} - {check_out_date.strftime("%b %d, %Y")}"

                    return None

                elif index.column() == 5:
                    return self._data[index.row()][index.column() + 1]

                elif index.column() == 6 or index.column() == 7:
                    return ""

                return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.ToolTipRole:
            if index.column() == 6:
                return "View reservation details?"
            elif index.column() == 7:
                return "Check in?"

        if role == self.BUTTON_ENABLED_ROLE and index.column() == 7:
            reservation_status = self._data[index.row()][7]

            return reservation_status == "Pending"

        if self.view_mode == "billing_page_view" and role == self.BUTTON_ENABLED_ROLE and index.column() == 5:
            payment_status = self._data[index.row()][5]

            return payment_status in ["Not Paid", "Partially Paid"]

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
