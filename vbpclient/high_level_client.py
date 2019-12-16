import re
import getpass
import json

from .low_level_client import LowLevelClient
from .conf import Route
from .exceptions import ResourceNotFound
from .models import Geometry, \
    Obat, \
    Organization, \
    Project, \
    Weather, \
    MonoSimulationGroup, \
    GenericSimulationGroup


class OSSClient:
    """
    End User Interface.
    """
    def __init__(self,  url="https://oplus-back.openergy.fr", auth_path=None):
        """
        Parameters
        ----------
        url: str
            url of the oplus API you want to connect to
        auth_path: str
            optional, provide path to a json file containing a list ["user_name", "password"] to use. If None, the user
            is prompted for the answer
        """
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

        self.dev_client = LowLevelClient(credentials=(login, password), host=url, port=port)

    def create_organization(self, **data):
        """
        Parameters
        ----------
        data: dict

        Returns
        -------
        Organization
        """
        json_data = self.dev_client.create(Route.organization, data)
        return Organization(json_data, self)

    def iter_organization(self, **params):
        """
        Parameters
        ----------
        params: dict

        Returns
        -------
        typing.Iterable[Organization]
        """
        json_data = self.dev_client.list_iter_all(Route.organization, params=params)
        return (
            Organization(element, self) for element in json_data
        )

    def list_organization(self, **params):
        """
        Parameters
        ----------
        params: dict

        Returns
        -------
        typing.List[Organization]
        """
        return list(self.iter_organization(**params))

    def get_organization(self, organization_name):
        """
        Parameters
        ----------
        organization_name: str

        Returns
        -------
        Organization
        """
        json_data = self.dev_client.list_iter_all(Route.organization)
        for org_data in json_data:
            if org_data["name"] == organization_name:
                break
        else:
            raise ResourceNotFound(f"Organization with name '{organization_name}' was not found.")

        return Organization(org_data, self)

    def get_organization_by_id(self, organization_id):
        """
        Parameters
        ----------
        organization_id: str

        Returns
        -------
        Organization
        """
        json_data = self.dev_client.retrieve(Route.organization, organization_id)
        return Organization(json_data, self)

    def iter_project(self, **params):
        """
        Parameters
        ----------
        params: dict

        Returns
        -------
        typing.Iterable[Project]
        """
        json_data = self.dev_client.list_iter_all(Route.project, params=params)
        return (
            Project(element, self) for element in json_data
        )

    def list_project(self, **params):
        """
        Parameters
        ----------
        params: dict

        Returns
        -------
        typing.List[Project]
        """
        return list(self.iter_project(**params))

    def get_project_by_id(self, project_id):
        """
        Parameters
        ----------
        project_id: str

        Returns
        -------
        Project
        """
        json_data = self.dev_client.retrieve(Route.project, project_id)
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

    def get_geometry_by_id(self, geometry_id):
        """
        Parameters
        ----------
        geometry_id: str

        Returns
        -------
        Geometry
        """
        json_data = self.dev_client.retrieve(Route.geometry, geometry_id)
        return Geometry(json_data, self)

    def get_weather_by_id(self, weather_id):
        """
        Parameters
        ----------
        weather_id: str

        Returns
        -------
        Weather
        """
        json_data = self.dev_client.retrieve(Route.weather, weather_id)
        return Weather(json_data, self)

    def get_obat_by_id(self, obat_id):
        """
        Parameters
        ----------
        obat_id: str

        Returns
        -------
        Obat
        """
        json_data = self.dev_client.retrieve(Route.obat, obat_id)
        return Obat(json_data, self)

    def get_mono_simulation_group_by_id(self, mono_simulation_group_id):
        """
        Parameters
        ----------
        mono_simulation_group_id: str

        Returns
        -------
        MonoSimulationGroup
        """
        json_data = self.dev_client.retrieve(Route.mono_simulation_group, mono_simulation_group_id)
        return MonoSimulationGroup(json_data, self)

    def get_generic_simulation_group_by_id(self, generic_simulation_group_id):
        """
        Parameters
        ----------
        generic_simulation_group_id: str

        Returns
        -------
        GenericSimulationGroup
        """
        json_data = self.dev_client.retrieve(Route.generic_simulation_group, generic_simulation_group_id)
        return GenericSimulationGroup(json_data, self)
