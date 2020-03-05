from ._import_export_base import BaseModel


class Floorspace(BaseModel):
    def upload(self, buffer_or_path):
        upload_url = self.detail_action("upload_url")["blob_url"]
        self.client.rest_client.upload(upload_url, buffer_or_path)

    def download(self, buffer_or_path=None):
        download_url = self.detail_action("read_blob_url")["blob_url"]
        self.client.rest_client.download(download_url, buffer_or_path=buffer_or_path)
