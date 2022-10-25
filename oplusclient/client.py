from .rest_client import RestClient
from .endpoints import BaseEndpoint
from . import models


class Client:
    def __init__(self, api_token=None, base_url=None):
        """
        Parameters
        ----------
        api_token
        base_url: default https://oplus-back.openergy.fr/api/v1
        """
        self.rest_client: RestClient = RestClient(api_token=api_token, base_url=base_url)

        # geometry
        self.geometry = BaseEndpoint(
            self,
            "ossgeometry/geometries",
            model_cls=models.Geometry)
        self.floorspace = BaseEndpoint(
            self,
            "ossgeometry/floorspaces",
            model_cls=models.Floorspace)

        # obat
        self.obat = BaseEndpoint(
            self,
            "ossbat/obats",
            model_cls=models.Obat)

        # weather
        self.weather = BaseEndpoint(
            self,
            "ossweather/weathers",
            model_cls=models.Weather)

        self.generic_weather_series = BaseEndpoint(
            self,
            "ossweather/generic_weather_series",
            model_cls=models.ImportExportBaseModel)

        self.historical_weather_series = BaseEndpoint(
            self,
            "ossweather/historical_weather_series",
            model_cls=models.ImportExportBaseModel)

        self.openergy_historical_weather_series = BaseEndpoint(
            self,
            "ossweather/openergy_historical_weather_series",
            model_cls=models.ImportExportBaseModel
        )

        # simulations
        self.simulation_group = BaseEndpoint(
            self,
            "osssimulations/simulation_groups",
            models.SimulationGroup)
        self.multi_simulation_group = BaseEndpoint(
            self,
            "osssimulations/multi_simulation_groups",
            models.MultiSimulationGroup)
        self.mono_simulation_group = BaseEndpoint(
            self,
            "osssimulations/mono_simulation_groups",
            models.MonoSimulationGroup)
        self.generic_simulation_group = BaseEndpoint(
            self,
            "osssimulations/generic_simulation_groups",
            models.GenericSimulationGroup)

        # oteams
        self.user = BaseEndpoint(self, "oteams/users")
        self.organization = BaseEndpoint(self, "oteams/organizations", model_cls=models.Organization)
        self.project = BaseEndpoint(self, "oteams/projects", model_cls=models.Project)
        self.user_organization_permission = BaseEndpoint(self, "oteams/user_organization_permissions")

    def close(self):
        self.rest_client.close()

    def get_organization(self, name):
        """
        Get organization by name.

        Parameters
        ----------
        name: str

        Returns
        -------
        oplusclient.models.Organization
        """
        return self.organization.get_one_and_only_one(filter_by=dict(name=name))

    def get_project(self, organization_name, project_name):
        """
        Get project by organization and name.

        Parameters
        ----------
        organization_name: str
        project_name: str

        Returns
        -------
        oplusclient.models.Project
        """
        organization = self.get_organization(organization_name)
        return self.project.get_one_and_only_one(filter_by=dict(organization=organization.id, name=project_name))
