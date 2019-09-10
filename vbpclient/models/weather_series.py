from ..conf import Route
from . import ProjectChild


class WeatherSeries(ProjectChild):
    _struct_type = "Generic Weather Series"
    _resource = Route.weather

    def import_epw(self, path):
        """
        uploads and imports Epw weather file.
        """
        self._client._dev_client.upload(Route.weather, self.id, path)
        self._client._dev_client.import_data(Route.weather, self.id, "epw")


