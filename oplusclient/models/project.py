from ..exceptions import RecordNotFoundError
from ._import_export_base import BaseModel


class Project(BaseModel):
    def get_organization(self):
        return self._get_related("organization", self.client.organization)
