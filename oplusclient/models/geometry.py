from .import_export_base import ImportExportBaseModel


class Geometry(ImportExportBaseModel):
    def get_floorspace(self):
        """
        Get associated floorspace.

        Returns
        -------
        oplusclient.models.Floorspace
        """
        return self._get_related("floorspace", self.client.floorspace)

    def import_file(self, buffer_or_path, import_format="ogw"):
        """
        Upload a file and import it in the platform.

        Parameters
        ----------
        buffer_or_path: str
            path of the file to upload
        import_format: str
            format of the file ('idf', 'gbxml', 'ogw'), not relevant for floorspace geometries
        """
        # upload
        if self.format == "floorspace":
            import_format = "floorspace"
            self.get_floorspace().upload(buffer_or_path)
        else:
            if import_format is None:
                raise ValueError("For non-floorspace geometries, the format must be specified when importing.")
            self._upload(buffer_or_path)
        # import
        self._import(import_format)

    def download_ogw(self, buffer_or_path=None):
        """
        Download this geometry's ogw (Openergy Geometry Wireframe) file.

        Parameters
        ----------
        buffer_or_path: str
            path of the file, if None returns the file content as bytes

        Returns
        -------
        bytes
        """
        self._check_empty()
        return self._download(buffer_or_path=buffer_or_path)

    def download_threejs(self, buffer_or_path=None):
        """
        Download this geometry's ogw (Openergy Geometry Wireframe) file.

        Parameters
        ----------
        buffer_or_path: str
            path of the file, if None returns the file content as bytes

        Returns
        -------
        bytes
        """
        self._check_empty()
        return self._download(buffer_or_path=buffer_or_path, path="threejs_blob_url")

    def download_source_file(self, buffer_or_path=None):
        """
        Download this geometry's ogw (Openergy Geometry Wireframe) file.

        Parameters
        ----------
        buffer_or_path: str
            path of the file, if None returns the file content as bytes

        Returns
        -------
        bytes
        """
        self._check_empty()
        return self._download(buffer_or_path=buffer_or_path, path="source_blob_url")

    def _check_empty(self):
        if self.empty:
            self.reload()
            if self.empty:
                raise ValueError("Geometry is empty.")
