from ..conf import Route
from . import ProjectChild


class Geometry(ProjectChild):
    _struct_type = "Geometry"
    _resource = Route.geometry

    def import_geometry(self, path, format=None):
        """
        uploads and imports geometry.
        """
        # upload
        if self.format == "floorspace":
            upload_resource = Route.floorspace
            upload_id = self.floorspace
            format = self.format
        else:
            upload_resource = Route.geometry
            upload_id = self.id
            if format is None:
                raise ValueError("For non-floorspace geometries, the format must be specified when importing.")
        self._client._dev_client.upload(upload_resource, upload_id, path)
        # import
        self._client._dev_client.import_data(Route.geometry, self.id, format)

    def download_ogw(self, path=None):
        if self.empty:
            raise ValueError("Geometry is empty, cannot download Ogw. Please import first.")
        return self._client._dev_client.download(Route.geometry, self.id, path=path)

    def download_floorspace(self, path=None):
        if self.format != "floorspace":
            raise ValueError("Cannot download floorspace if the geometry format is not floorspace")
        return self._client._dev_client.download(Route.floorspace, self.floorspace, path=path, detail_route="read_blob_url")
