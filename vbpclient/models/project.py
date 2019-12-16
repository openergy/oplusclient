from ..conf import Route
from ..struct import APIMapping
from ..exceptions import ResourceNotFound
from . import Weather, Obat, MonoSimulationGroup, Geometry, GenericSimulationGroup


class Project(APIMapping):
    _struct_type = "Project"
    _resource = Route.project

    def get_organization_id(self):
        organization_link = self.organization
        if isinstance(organization_link, str):
            return organization_link
        else:
            return organization_link.id

    def get_organization(self):
        return self._client.get_organization_by_id(self.get_organization_id())

    def _create_child(self, cls, **data):
        if "project" in data:
            raise ValueError(f"Cannot pass a project id, using '{self.id}'.")
        data["project"] = self.id
        json_data = self._client.dev_client.create(cls._resource, data)
        return cls(json_data, self._client)

    def _get_child(self, cls, name):
        candidates = list(filter(
            lambda child: child.name == name,
            cls._dev_iter(self._client, project=self.id)
        ))
        if len(candidates) != 1:
            raise ResourceNotFound(f"{cls.__name__} '{name}' not be found.")
        return candidates[0]

    def _iter_child(self, cls, **params):
        if "project" in params:
            raise ValueError(f"Cannot pass a project id, using '{self.id}'.")
        params["project"] = self.id
        return cls._dev_iter(self._client, **params)

    def create_geometry(self, name, geometry_format, **data):
        """
        Parameters
        ----------
        name
        geometry_format
        data

        Returns
        -------
        Geometry
        """
        if geometry_format not in ("floorspace", "import"):
            raise ValueError(f"'format' keyword should be one of ('import', 'floorspace') and not '{geometry_format}'.")
        data["name"] = name
        data["format"] = geometry_format
        return self._create_child(Geometry, **data)

    def get_geometry(self, geometry_name):
        """
        Returns
        -------
        Geometry
        """
        return self._get_child(Geometry, geometry_name)

    def iter_geometry(self, **params):
        return self._iter_child(Geometry, **params)

    def list_geometry(self, **params):
        """
        Parameters
        ----------
        params

        Returns
        -------
        typing.List[Geometry]
        """
        return list(self.iter_geometry(**params))

    def create_obat(self, name, **data):
        """
        Parameters
        ----------
        name: str
        data

        Returns
        -------
        Obat
        """
        data["name"] = name
        return self._create_child(Obat, **data)

    def get_obat(self, obat_name):
        return self._get_child(Obat, obat_name)

    def iter_obat(self, **params):
        return self._iter_child(Obat, **params)

    def list_obat(self, **params):
        """
        Parameters
        ----------
        params

        Returns
        -------
        typing.List[Obat]
        """
        return list(self.iter_obat(**params))

    def create_weather(self, name, **data):
        """
        Returns
        -------
        Weather
        """
        data["name"] = name
        if "format" not in data:
            data["format"] = "generic"
        return self._create_child(Weather, **data)

    def get_weather(self, weather_series_name):
        """
        Returns
        -------
        Weather
        """
        return self._get_child(Weather, weather_series_name)

    def iter_weather(self, **params):
        return self._iter_child(Weather, **params)

    def list_weather(self, **params):
        """
        Parameters
        ----------
        params

        Returns
        -------
        typing.List[Weather]
        """
        return list(self.iter_weather(**params))

    def create_mono_simulation_group(self, name, **data):
        """
        Parameters
        ----------
        name: str
        data

        Returns
        -------
        MonoSimulationGroup
        """
        data["name"] = name
        return self._create_child(MonoSimulationGroup, **data)

    def get_mono_simulation_group(self, mono_simulation_group_name):
        """
        Parameters
        ----------
        mono_simulation_group_name: str

        Returns
        -------
        MonoSimulationGroup
        """
        return self._get_child(MonoSimulationGroup, mono_simulation_group_name)

    def iter_mono_simulation_group(self, **params):
        return self._iter_child(MonoSimulationGroup, **params)

    def list_mono_simulation_group(self, **params):
        return list(self.iter_mono_simulation_group(**params))

    def create_generic_simulation_group(self, name, **data):
        data["name"] = name
        return self._create_child(GenericSimulationGroup, **data)

    def get_generic_simulation_group(self, generic_simulation_group_name):
        return self._get_child(GenericSimulationGroup, generic_simulation_group_name)

    def iter_generic_simulation_group(self, **params):
        return self._iter_child(GenericSimulationGroup, **params)

    def list_generic_simulation_group(self, **params):
        return list(self.iter_generic_simulation_group(**params))


