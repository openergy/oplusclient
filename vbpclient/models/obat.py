from ..conf import Route
from . import ProjectChild


class Obat(ProjectChild):
    _struct_type = "Obat"
    _resource = Route.obat

    def import_excel(self, path):
        self._client._dev_client.upload(Route.obat, self.id, path)
        self._client._dev_client.import_data(Route.obat, self.id, "xlsx")

    def download_obat(self, path=None):
        return self._client._dev_client.download(Route.obat, self.id, path=path)