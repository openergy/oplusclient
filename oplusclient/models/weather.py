from .import_export_base import ImportExportBaseModel


class Weather(ImportExportBaseModel):
    def get_weather_series(self):
        """
        Get the weather series model.

        Returns
        -------
        oplusclient.models.ImportExportBaseModel
        """
        if self.format == "generic":
            return self._get_related("generic_weather_series", self.client.generic_weather_series)
        elif self.format == "historical":
            return self._get_related("historical_weather_series", self.client.historical_weather_series)
        elif self.format == "openergy_historical":
            return self._get_related(
                "openergy_historical_weather_series",
                self.client.openergy_historical_weather_series
            )
        else:
            raise NotImplementedError(f"Unknown format: {self.format}")

    def import_file(self, buffer_or_path, import_format="ow", csv_separator=",", csv_decimal="."):
        """
        Upload and import an obat file to the platform.

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
            self._upload(buffer_or_path)
            self._import(import_format)
        else:
            series = self.get_weather_series()
            # TODO: do not use private methods
            series._upload(buffer_or_path)
            series._import(import_format, csv_separator=csv_separator, csv_decimal=csv_decimal)

    def export(self, export_format, buffer_or_path=None, csv_separator=",", csv_decimal="."):
        """
        Exports obat to specified format

        Parameters
        ----------
        export_format: str
            "csv", "epw"
        buffer_or_path: BytesIO like or string
        csv_separator: str
            separator used if the export_format is a csv file
        csv_decimal: str
            decimal used if the export_format is a csv file

        Returns
        -------
        bytes
        """
        if export_format == "ow":
            return self._export(export_format=export_format, buffer_or_path=buffer_or_path)
        else:
            series = self.get_weather_series()
            # TODO: do not use private methods
            return series._export(
                export_format=export_format,
                params=dict(csv_separator=csv_separator, csv_decimal=csv_decimal),
                buffer_or_path=buffer_or_path
            )

    def clear_weather_series(self):
        """Clear the weather series."""
        series = self.get_weather_series()
        series.detail_action("clear", "delete")
