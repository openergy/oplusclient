from .import_export_base import BaseModel


class Floorspace(BaseModel):
    def upload(self, buffer_or_path):
        """
        Upload a new version of this floorspace (will replace the current one).

        Parameters
        ----------
        buffer_or_path: str or typing.TextIO
        """
        upload_url = self.detail_action("upload_url")["blob_url"]
        self.client.rest_client.upload(upload_url, buffer_or_path)

    def download(self, buffer_or_path=None):
        """
        Download this floorspace.

        Will save the floorspace to buffer_or_path is not None, else will return the content as bytes.

        Parameters
        ----------
        buffer_or_path: str or typing.TextIO or None

        Returns
        -------
        bytes or None
        """
        download_url = self.detail_action("read_blob_url")["blob_url"]
        return self.client.rest_client.download(download_url, buffer_or_path=buffer_or_path)
