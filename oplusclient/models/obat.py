import json
from .import_export_base import ImportExportBaseModel


class Obat(ImportExportBaseModel):
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
                self.client.rest_client.update("ossbat/obat_contents", self.id, data=json.load(buffer_or_path))
            else:
                with open(buffer_or_path, "r") as f:
                    self.client.rest_client.update("ossbat/obat_contents", self.id, data=json.load(f))
        else:
            self._upload(buffer_or_path)
            self._import(import_format)

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
        return self._download(buffer_or_path=buffer_or_path)

    def export(self, export_format, buffer_or_path=None):
        """
        Exports obat to specified format

        Parameters
        ----------
        export_format: str
            only 'xlsx' available
        buffer_or_path: BytesIO like or string

        Returns
        -------
        bytes
        """
        return self._export(export_format=export_format, buffer_or_path=buffer_or_path)
