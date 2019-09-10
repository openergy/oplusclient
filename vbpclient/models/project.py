from ..conf import Route
from ..struct import APIMapping
from ..exceptions import ResourceNotFound
from . import WeatherSeries, Obat, MonoSimulationGroup, Geometry


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
        json_data = self._client._dev_client.create(cls._resource, data)
        return cls(json_data, self._client)

    def _get_child(self, cls, name):
        candidates = list(filter(
            lambda child: child.name == name,
            cls._dev_iter(self._client._dev_client, project=self.id)
        ))
        if len(candidates) != 1:
            raise ResourceNotFound(f"{cls.__name__} '{name}' not be found.")
        return candidates[0]

    def _iter_child(self, cls, **params):
        if "project" in params:
            raise ValueError(f"Cannot pass a project id, using '{self.id}'.")
        params["project"] = self.id
        return cls._dev_iter(self._client._dev_client, **params)

    def create_geometry(self, name, geometry_format, **data):
        if geometry_format not in ("floorspace", "import"):
            raise ValueError(f"'format' keyword should be one of ('import', 'floorspace') and not '{geometry_format}'.")
        data["name"] = name
        data["format"] = geometry_format
        return self._create_child(Geometry, **data)

    def get_geometry(self, geometry_name):
        return self._get_child(Geometry, geometry_name)

    def iter_geometry(self, **params):
        return self._iter_child(Geometry, **params)

    def list_geometry(self, **params):
        return list(self.iter_geometry(**params))

    def create_obat(self, name, **data):
        data["name"] = name
        return self._create_child(Obat, **data)

    def get_obat(self, obat_name):
        return self._get_child(Obat, obat_name)

    def iter_obat(self, **params):
        return self._iter_child(Obat, **params)

    def list_obat(self, **params):
        return list(self.iter_obat(**params))

    def create_weather_series(self, name, **data):
        data["name"] = name
        return self._create_child(WeatherSeries, **data)

    def get_weather_series(self, weather_series_name):
        return self._get_child(WeatherSeries, weather_series_name)

    def iter_weather_series(self, **params):
        return self._iter_child(WeatherSeries, **params)

    def list_weather_series(self, **params):
        return list(self.iter_weather_series(**params))

    def create_mono_simulation_group(self, name, **data):
        data["name"] = name
        return self._create_child(MonoSimulationGroup, **data)

    def get_mono_simulation_group(self, mono_simulation_group_name):
        return self._get_child(MonoSimulationGroup, mono_simulation_group_name)

    def iter_mono_simulation_group(self, **params):
        return self._iter_child(MonoSimulationGroup, **params)

    def list_mono_simulation_group(self, **params):
        return list(self.iter_mono_simulation_group(**params))


