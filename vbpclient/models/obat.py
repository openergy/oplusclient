import json

from ..conf import Route
from . import ProjectChild


class Obat(ProjectChild):
    _struct_type = "Obat"
    _resource = Route.obat

    def import_file(self, buffer_or_path, import_format="obat"):
        """
        Upload and import an obat file to the platform

        Parameters
        ----------
        buffer_or_path: str
            path to the file
        import_format: str
            format of the file ('xlsx' or 'obat')
        """
        if import_format == "obat":
            if hasattr(buffer_or_path, "read"):
                self._client.dev_client.client.update(Route.obat_content, self.id, data=json.load(buffer_or_path))
            else:
                with open(buffer_or_path, "r") as f:
                    self._client.dev_client.client.update(Route.obat_content, self.id, data=json.load(f))
        else:
            self._client.dev_client.upload(Route.obat, self.id, buffer_or_path)
            self._client.dev_client.import_data(Route.obat, self.id, import_format)

    def download_obat(self, buffer_or_path=None):
        """
        Download the obat file from the platform (as json)

        Parameters
        ----------
        buffer_or_path: str
            path of the file to download to, if None the content is returned as bytes

        Returns
        -------
        bytes
        """
        return self._client.dev_client.download(Route.obat, self.id, buffer_or_path=buffer_or_path)

    def export(self, export_format, buffer_or_path=None):
        """
        Exports obat to specified format

        Parameters
        ----------
        export_format: str
        buffer_or_path: BytesIO like or string

        Returns
        -------
        bytes
        """
        return self._client.dev_client.export(
            self._resource,
            self.id,
            export_format=export_format,
            buffer_or_path=buffer_or_path
        )
