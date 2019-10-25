from ..conf import Route
from . import ProjectChild


class Weather(ProjectChild):
    _struct_type = "Generic Weather"
    _resource = Route.weather

    def _get_series_route_and_id(self):
        if self.format == "generic":
            return Route.generic_weather_series, self.generic_weather_series
        elif self.format == "historical":
            return Route.historical_weather_series, self.historical_weather_series
        else:
            raise ValueError("Unknown format")

    def download_ow(self, path=None):
        return self._client._dev_client.export(Route.weather, self.id, "export_data", path=path)

    def import_ow(self, path):
        self._client._dev_client.upload(Route.weather, self.id, path)
        self._client._dev_client.import_data(Route.weather, self.id, "ow")

    def import_epw(self, path):
        """
        uploads and imports Epw weather file.
        """
        route, series_id = self._get_series_route_and_id()
        self._client._dev_client.upload(route, series_id, path)
        self._client._dev_client.import_data(route, series_id, "epw")

    def download_csv(self, path=None):
        route, series_id = self._get_series_route_and_id()
        return self._client._dev_client.export(route, series_id, export_format="csv", path=path)
