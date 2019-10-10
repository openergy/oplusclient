import re
import getpass
import json

from .low_level_client import LowLevelClient
from .conf import Route
from .exceptions import ResourceNotFound
from .tasker import Task
from .models import Geometry, \
    Obat, \
    Organization, \
    Project, \
    Weather


class OSSClient:
    """
    End User Interface.
    """
    def __init__(self, auth_path=None, url=None, url_path=None):
        """
        Prompts the user for login and password
        """
        if url is None:
            if url_path is None:
                raise RuntimeError("Unspecified url.")
            with open(url_path) as f:
                url = f.read().strip()

        if auth_path is not None:
            login, password = json.load(open(auth_path))
        else:
            login = input("Login: ")
            password = getpass.getpass()

        match = re.match(r"(.*):(\d+)/?$", url)
        if match is not None:
            url = match.group(1)
            port = int(match.group(2))
        else:
            port = 443

        self._dev_client = LowLevelClient(credentials=(login, password), host=url, port=port)

    def create_organization(self, **data):
        json_data = self._dev_client.create(Route.organization, data)
        return Organization(json_data, self)

    def iter_organization(self, **params):
        json_data = self._dev_client.list_iter_all(Route.organization, params=params)
        return (
            Organization(element, self) for element in json_data
        )

    def list_organization(self, **params):
        return list(self.iter_organization(**params))

    def get_organization(self, organization_name):
        json_data = self._dev_client.list_iter_all(Route.organization)
        for org_data in json_data:
            if org_data["name"] == organization_name:
                break
        else:
            raise ResourceNotFound(f"Organization with name '{organization_name}' was not found.")

        return Organization(org_data, self)

    def get_organization_by_id(self, organization_id):
        json_data = self._dev_client.retrieve(Route.organization, organization_id)
        return Organization(json_data, self)

    def iter_project(self, **params):
        json_data = self._dev_client.list_iter_all(Route.project, params=params)
        return (
            Project(element, self) for element in json_data
        )

    def list_project(self, **params):
        return list(self.iter_project(**params))

    def get_project_by_id(self, project_id):
        json_data = self._dev_client.retrieve(Route.project, project_id)
        return Project(json_data, self)

    def get_project(self, organization_name, project_name):
        """
        Parameters
        ----------
        organization_name: str
        project_name: str

        Returns
        -------
        Project
        """
        return self.get_organization(organization_name).get_project(project_name)

