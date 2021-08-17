from .import_export_base import BaseModel


class Project(BaseModel):
    def get_organization(self):
        """
        Get this project organization.

        Returns
        -------
        oplusclient.models.Organization
        """
        return self._get_related("organization", self.client.organization)

    def create_geometry(self, name, format, comment=None, rules_reference_surface=None):
        """
        Create a geometry in this project.

        Parameters
        ----------
        name: str
        format: str
            floorspace or import
        comment: str
        rules_reference_surface: float

        Returns
        -------
        oplusclient.models.Geometry
        """
        data = {k: v for k, v in (
            ("comment", comment),
            ("rules_reference_surface", rules_reference_surface)
        ) if v is not None}
        return self.client.geometry.create(name=name, format=format, project=self.id, **data)

    def get_geometry(self, name):
        """
        Get geometry by name.

        Parameters
        ----------
        name: str

        Returns
        -------
        oplusclient.models.Geometry
        """
        return self._get_by_filter(self.client.geometry, name)

    def list_geometries(self):
        """
        List geometries in this project.

        Returns
        -------
        list of oplusclient.models.Geometry
        """
        return self._list_by_filter(self.client.geometry)

    def get_obat(self, name):
        """
        Get obat in this project.

        Parameters
        ----------
        name: str

        Returns
        -------
        oplusclient.models.Obat
        """
        return self._get_by_filter(self.client.obat, name)

    def create_obat(self, name, comment=None):
        """
        Create a new thermal model in this project.

        Parameters
        ----------
        name: str
        comment: str

        Returns
        -------
        oplusclient.models.Obat
        """
        data = {k: v for k, v in (
            ("comment", comment),
        ) if v is not None}
        return self.client.obat.create(name=name, project=self.id, **data)

    def list_obats(self):
        """
        List thermal models in this project.

        Returns
        -------
        list of oplusclient.models.Obat
        """
        return self._list_by_filter(self.client.obat)

    def get_weather(self, name):
        """
        Get weather in this project.

        Parameters
        ----------
        name: str

        Returns
        -------
        oplusclient.models.Weather
        """
        return self._get_by_filter(self.client.weather, name)

    def create_weather(
            self,
            name,
            format,
            comment=None,
            location_time_zone_ref=None,
            sizing=None,
            site_conditions=None,
            location_latitude=None,
            location_longitude=None,
            location_altitude=None
    ):
        """
        Create a new weather in this project.

        Parameters
        ----------
        name
        format
        comment: str
        location_time_zone_ref: str
        sizing: dict
        site_conditions: dict
        location_latitude: float
        location_longitude: float
        location_altitude: float

        Returns
        -------
        oplusclient.models.Weather
        """
        data = {k: v for k, v in (
            ("comment", comment),
            ("location_time_zone_ref", location_time_zone_ref),
            ("sizing", sizing),
            ("site_conditions", site_conditions),
            ("location_latitude", location_latitude),
            ("location_longitude", location_longitude),
            ("location_altitude", location_altitude),
        ) if v is not None}
        return self.client.weather.create(project=self.id, name=name, format=format, **data)

    def list_weathers(self):
        """
        List weathers in this project.

        Returns
        -------
        list of oplusclient.models.Weather
        """
        return self._list_by_filter(self.client.weather)

    # TODO: accept more input types ()
    def create_mono_simulation_group(
        self,
        name,
        comment=None,
        config_variant=None,
        config_start=None,
        config_end=None,
        config_obat=None,
        config_geometry=None,
        config_weather=None,
        config_outputs_detail_nfen12831=None,
        config_outputs_report=None
    ):
        """
        Create a mono_simulation_group in this project.

        Parameters
        ----------
        name: str
        comment: str
        config_variant: str
        config_start: str
            simulation start date
        config_end: str
            simulation end date
        config_obat: str
            simulation's obat id
        config_geometry: str
            simulation's geometry id
        config_weather: str
            simulations's weather id
        config_outputs_detail_nfen12831: bool
        config_outputs_report: bool

        Returns
        -------
        oplusclient.models.MonoSimulationGroup
        """
        data = {k: v for k, v in (
            ("comment", comment),
            ("config_variant", config_variant),
            ("config_start", config_start),
            ("config_end", config_end),
            ("config_obat", config_obat),
            ("config_geometry", config_geometry),
            ("config_weather", config_weather),
            ("config_outputs_detail_nfen12831", config_outputs_detail_nfen12831),
            ("config_outputs_report", config_outputs_report)
        ) if v is not None}
        return self.client.mono_simulation_group.create(name=name, project=self.id, **data)

    def get_mono_simulation_group(self, name):
        """
        Get mono_simulation_group by name.

        Parameters
        ----------
        name: str

        Returns
        -------
        oplusclient.models.MonoSimulationGroup
        """
        return self._get_by_filter(self.client.mono_simulation_group, name)

    def list_mono_simulation_groups(self):
        """
        List mono_simulation_groups in this project.

        Returns
        -------
        list of oplusclient.models.MonoSimulationGroup
        """
        return self._list_by_filter(self.client.mono_simulation_group)

    def create_multi_simulation_group(
            self,
            name,
            comment=None
    ):
        """
        Create a multi_simulation_group in this project.

        Parameters
        ----------
        name: str
        comment: str

        Returns
        -------
        oplusclient.models.MultiSimulationGroup
        """
        data = {k: v for k, v in (
            ("comment", comment),
        ) if v is not None}
        return self.client.multi_simulation_group.create(name=name, project=self.id, **data)

    def get_multi_simulation_group(self, name):
        """
        Get multi_simulation_group by name.

        Parameters
        ----------
        name: str

        Returns
        -------
        oplusclient.models.MultiSimulationGroup
        """
        return self._get_by_filter(self.client.multi_simulation_group, name)

    def list_multi_simulation_groups(self):
        """
        List multi_simulation_groups in this project.

        Returns
        -------
        list of oplusclient.models.MultiSimulationGroup
        """
        return self._list_by_filter(self.client.multi_simulation_group)

    def create_generic_simulation_group(
            self,
            name,
            comment=None
    ):
        """
        Create a generic_simulation_group in this project.

        Parameters
        ----------
        name: str
        comment: str

        Returns
        -------
        oplusclient.models.GenericSimulationGroup
        """
        data = {k: v for k, v in (
            ("comment", comment),
        ) if v is not None}
        return self.client.generic_simulation_group.create(name=name, project=self.id, **data)

    def get_generic_simulation_group(self, name):
        """
        Get generic_simulation_group by name.

        Parameters
        ----------
        name: str

        Returns
        -------
        oplusclient.models.GenericSimulationGroup
        """
        return self._get_by_filter(self.client.generic_simulation_group, name)

    def list_generic_simulation_groups(self):
        """
        List generic_simulation_groups in this project.

        Returns
        -------
        list of oplusclient.models.GenericSimulationGroup
        """
        return self._list_by_filter(self.client.generic_simulation_group)

    def _list_by_filter(self, endpoint):
        return list(endpoint.iter(filter_by=dict(project=self.id)))

    def _get_by_filter(self, endpoint, name):
        return endpoint.get_one_and_only_one(filter_by=dict(project=self.id, name=name))
