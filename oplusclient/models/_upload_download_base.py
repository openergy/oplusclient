from ..task import Task
from .base import BaseModel


class ImportExportBaseModel(BaseModel):
    def _upload(self, buffer_or_path, path="upload_url"):
        upload_url = self.detail_action(path)["blob_url"]
        self.client.rest_client.upload(upload_url, buffer_or_path)

    def _download(self, buffer_or_path=None, path="blob_url"):
        download_url = self.detail_action(path)["blob_url"]
        return self.client.rest_client.download(download_url, buffer_or_path=buffer_or_path)

    def _import(self, import_format, **kwargs):
        response = self.detail_action(
            "PATCH",
            "import_data",
            data=dict(import_format=import_format, **kwargs),
        )
        if response:
            task_id = response["user_task"]
            import_task = Task(task_id, self)
            success = import_task.wait_for_completion(period=100)
            if not success:
                raise RuntimeError(
                    f"Import failed. Error:\n"
                    f"{import_task.message}"
                )

    def _export(
            self,
            resource,
            resource_id,
            detail_route="export_data",
            export_format=None,
            params=None,
            buffer_or_path=None
    ):
        params = dict() if params is None else params
        if export_format is not None:
            params["export_format"] = export_format
        response = self.detail_action(resource, resource_id, "GET", detail_route, params=params)
        export_task = Task(response["user_task"], self)
        success = export_task.wait_for_completion(period=100)
        if not success:
            raise RuntimeError(f"Import failed. Error:\n{export_task.message}\n{export_task.response['_out_text']}")
        download_url = export_task.response["data"]["blob_url"]
        return self.client.dev_client.download(download_url, buffer_or_path=buffer_or_path)
