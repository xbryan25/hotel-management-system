from PyQt6.QtCore import QAbstractTableModel, Qt


class AvailedServicesModel:
    def __init__(self, availed_services_list):
        super().__init__()

        self._availed_services = availed_services_list

    def get_all(self) -> list[dict]:
        return self._availed_services

    # def get_by_name(self, name: str) -> dict | None:
    #     for service in self._availed_services:
    #         if service["name"] == name:
    #             return service
    #     return None

    def add_availed_service(self, service):
        self._availed_services.append(service)

    def remove_availed_service_by_name(self, name: str):
        self._availed_services = [s for s in self._availed_services if s["name"] != name]

    def remove_availed_service_by_id(self, service_id: str):
        self._availed_services = [s for s in self._availed_services if s[0] != service_id]

    def is_service_availed(self, service_id):
        for availed_service in self._availed_services:
            if service_id == availed_service[0]:
                return True

        return False

    def get_availed_service_details(self, service_id):
        for availed_service in self._availed_services:
            if service_id == availed_service[0]:
                return availed_service

        return None

    def update_data(self, availed_services_list):
        self.beginResetModel()
        self._availed_services = availed_services_list
        self.endResetModel()

