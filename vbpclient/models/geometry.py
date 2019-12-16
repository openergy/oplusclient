from ..conf import Route
from . import ProjectChild


class Geometry(ProjectChild):
    _struct_type = "Geometry"
    _resource = Route.geometry

    def import_file(self, buffer_or_path, import_format="ogw"):
        """
        Upload a file and import it in the platform

        Parameters
        ----------
        buffer_or_path: str
            path of the file to upload
        import_format: str
            format of the file ('idf', 'gbxml', 'ogw'), not relevant for floorspace geometries
        """
        # upload
        if self.format == "floorspace":
            upload_resource = Route.floorspace
            upload_id = self.floorspace
            import_format = self.format
        else:
            upload_resource = Route.geometry
            upload_id = self.id
            if import_format is None:
                raise ValueError("For non-floorspace geometries, the format must be specified when importing.")
        self._client.dev_client.upload(upload_resource, upload_id, buffer_or_path)
        # import
        self._client.dev_client.import_data(Route.geometry, self.id, import_format)

    def download_ogw(self, buffer_or_path=None):
        """
        Download this geometry's ogw (Openergy Geometry Wireframe) file

        Parameters
        ----------
        buffer_or_path: str
            path of the file, if None returns the file content as bytes

        Returns
        -------
        bytes
        """
        if self.empty:
            raise ValueError("Geometry is empty, cannot download Ogw. Please import first.")
        return self._client.dev_client.download(Route.geometry, self.id, buffer_or_path=buffer_or_path)

    def download_floorspace(self, buffer_or_path=None):
        """
        Download this geometry's floorspace file

        Parameters
        ----------
        buffer_or_path: str
            path of the file, if None returns the file content as bytes

        Returns
        -------
        bytes
        """
        if self.format != "floorspace":
            raise ValueError("Cannot download floorspace if the geometry format is not floorspace")
        return self._client.dev_client.download(
            Route.floorspace,
            self.floorspace,
            buffer_or_path=buffer_or_path,
            detail_route="read_blob_url"
        )
