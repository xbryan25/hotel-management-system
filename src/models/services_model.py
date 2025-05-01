

class ServicesModel:
    def __init__(self, services_list: list[dict]):
        self._services = services_list

    def get_all(self) -> list[dict]:
        return self._services

    def get_by_name(self, name: str) -> dict | None:
        for service in self._services:
            if service["name"] == name:
                return service
        return None

    def add_service(self, service: dict):
        self._services.append(service)

    def remove_service(self, name: str):
        self._services = [s for s in self._services if s["name"] != name]
