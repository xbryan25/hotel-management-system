from PyQt6.QtCore import QAbstractTableModel, Qt


class ServicesModel(QAbstractTableModel):
    BUTTON_ENABLED_ROLE = Qt.ItemDataRole.UserRole + 1

    def __init__(self, services_list: list[dict]):
        super().__init__()

        self._services = services_list

        self.columns = ["Service ID", "Service Name", "Rate", "", ""]

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

    def get_len_of_data(self):
        return len(self._services)

    def update_data(self, services):
        self.beginResetModel()
        self._services = services
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
            if index.column() == 3 or index.column() == 4:
                return ""
            else:
                return self._services[index.row()][index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.ToolTipRole:
            if index.column() == 3:
                return "View service details?"
            elif index.column() == 4:
                if self._services[index.row()][3] == 1:
                    return "Disable service?"

        if role == self.BUTTON_ENABLED_ROLE and index.column() == 4:
            is_service_active = self._services[index.row()][3]

            return is_service_active == 1

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)
