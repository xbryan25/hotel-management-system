from PyQt6.QtCore import QAbstractTableModel, Qt


class ReservationModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()

        self._data = data

    def rowCount(self, index=None):
        pass

    def columnCount(self, index=None):
        pass

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        pass

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        pass
