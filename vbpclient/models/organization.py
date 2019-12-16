from ..conf import Route
from ..struct import APIMapping
from ..exceptions import ResourceNotFound
from . import Project


class Organization(APIMapping):
    _struct_type = "Organization"
    _resource = Route.organization

    def get_project(self, project_name):
        candidates = list(filter(
            lambda p: p.name == project_name,
            self._client.iter_project(organization=self.id),
        ))
        if len(candidates) != 1:
            raise ResourceNotFound(f"Project '{project_name}' not found.")
        return candidates[0]

    def iter_project(self, **params):
        if "organization" in params:
            raise ValueError(f"Cannot pass an organization name or id, using '{self.id}'.")
        return filter(
            lambda p: p.get_organization_id() == self.id,
            self._client.iter_project(**params),
        )

    def list_project(self, **params):
        return list(self.iter_project(**params))

    def create_project(self, name, **data):
        if "organization" in data:
            raise ValueError(f"Cannot pass an organization id, using '{self.id}'.")
        data["organization"] = self.id
        data["name"] = name
        json_data = self._client.dev_client.create("oteams/projects", data)
        return Project(json_data, self._client)

    def __repr__(self):
        return f"<{self._struct_type} name='{self.name}'>"


