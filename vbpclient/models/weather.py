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

    def import_file(self, buffer_or_path, import_format="ow", csv_separator=",", csv_decimal="."):
        """
        Upload and import an obat file to the platform

        Parameters
        ----------
        import_format: str
            format of the file ('csv', 'epw' or 'ow')
        buffer_or_path: str
            path to the file
        csv_separator: str
            separator used if the import_format is a csv file
        csv_decimal: str
            decimal used if the import_format is a csv file
        """
        if import_format == "ow":
            self._client.dev_client.upload(Route.weather, self.id, buffer_or_path=buffer_or_path)
            self._client.dev_client.import_data(Route.weather, self.id, "ow")
        else:
            route, series_id = self._get_series_route_and_id()
            self._client.dev_client.upload(route, series_id, buffer_or_path)
            self._client.dev_client.import_data(
                route,
                series_id,
                import_format,
                csv_separator=csv_separator,
                csv_decimal=csv_decimal
            )

    def export(self, export_format, buffer_or_path=None, csv_separator=",", csv_decimal="."):
        """
        Exports obat to specified format

        Parameters
        ----------
        export_format: str
        buffer_or_path: BytesIO like or string
        csv_separator: str
            separator used if the import_format is a csv file
        csv_decimal: str
            decimal used if the import_format is a csv file

        Returns
        -------
        bytes
        """
        if export_format == "ow":
            return self._client.dev_client.export(Route.weather, self.id, "export_data", buffer_or_path=buffer_or_path)
        else:
            route, series_id = self._get_series_route_and_id()
            return self._client.dev_client.export(
                route,
                series_id,
                export_format=export_format,
                buffer_or_path=buffer_or_path,
                params=dict(csv_separator=csv_separator, csv_decimal=csv_decimal)
            )

