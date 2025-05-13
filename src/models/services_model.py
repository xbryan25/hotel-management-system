from PyQt6.QtCore import QAbstractTableModel, Qt


class ServicesModel(QAbstractTableModel):
    def __init__(self, services_list: list[dict]):
        super().__init__()

        self._services = services_list

        self.columns = ["Service Name", "Rate"]

    def get_all(self) -> list[dict]:
        return self._services

    def get_by_name(self, name: str) -> dict | None:
        for service in self._services:
            if service["name"] == name:
                return service
        return None

    def add_service(self, service: dict):
        self._services.append(service)

    def remove_service_by_name(self, name: str):
        self._services = [s for s in self._services if s["name"] != name]

    def remove_service_by_id(self, service_id: str):
        self._services = [s for s in self._services if s[0] != service_id]

    def update_data(self, services):
        self.beginResetModel()
        self._services = services
        self.endResetModel()

    # Only for dashboard
    def rowCount(self, index=None):
        return len(self._services)

    def columnCount(self, index=None):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return self._services[index.row()][index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
