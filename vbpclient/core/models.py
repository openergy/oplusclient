from .tasker import Task
from .conf import Route
from .struct import APIMapping
from .exceptions import ResourceNotFound, SimulationError


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
        json_data = self._client._dev_client.create("oteams/projects", data)
        return Project(json_data, self._client)

    def __repr__(self):
        return f"<{self._struct_type} name='{self.name}'>"


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
        return list(self.iter_mono_simulation_group(self, **params))


class ProjectChild(APIMapping):
    """
    Base class for objects directly related to Project.
    """
    @classmethod
    def get_id(cls, project, instance_or_str):
        if isinstance(instance_or_str, str):
            # interpreted as a name/ref
            child = project._get_child(cls, instance_or_str)
            return child.id
        elif isinstance(instance_or_str, cls):
            return instance_or_str.id
        else:
            raise ValueError(f"{instance_or_str} should be a model object or an id.")


    def get_project_id(self):
        project_link = self.project
        if isinstance(project_link, str):
            return project_link
        else:
            return project_link.id

    def get_project(self):
        return self._client.get_project_by_id(self.get_project_id())

    def __repr__(self):
        """
        Specializes __repr__ if
            `self.project` has an attribute `name`
        """
        project_link = self.project
        if isinstance(project_link, str):
            return super().__repr__()

        if not hasattr(project_link, "name"):
            return super().__repr__()

        else:
            return f"<{self._struct_type} name='{self.name}', project='{project_link.name}'>"


class Geometry(ProjectChild):
    _struct_type = "Geometry"
    _resource = Route.geometry

    def import_geometry(self, path):
        """
        uploads and imports geometry.
        """
        # upload
        if self.format == "floorspace":
            upload_resource = Route.floorspace
            upload_id = self.floorspace
        elif self.format == "import":
            upload_resource = Route.idf
            upload_id = self.id
        else:
            raise NotImplementedError(f"Import for '{self.format}' was not implemented.")
        self._client._dev_client.upload(upload_resource, upload_id, "save_blob_url", path)
        # import
        self._client._dev_client.import_data(Route.geometry, self.id, self.format)


class Obat(ProjectChild):
    _struct_type = "Obat"
    _resource = Route.obat

    def import_excel(self, path):
        self._client._dev_client.upload(Route.obat, self.id, "upload_url", path)
        self._client._dev_client.import_data(Route.obat, self.id, "xlsx")


class WeatherSeries(ProjectChild):
    _struct_type = "Generic Weather Series"
    _resource = Route.weather

    def import_epw(self, path):
        """
        uploads and imports Epw weather file.
        """
        self._client._dev_client.upload(Route.weather, self.id, "import_upload_url", path)
        self._client._dev_client.import_data(Route.weather, self.id, "epw")


class MonoSimulationGroup(ProjectChild):
    _struct_type = "Mono Simulation Group"
    _simulations_resource = Route.mono_simulation_group + "/{}/simulations"
    _resource = Route.mono_simulation_group

    def update(self, **data):
        project = self.get_project()

        if "config_weather" in data:
            data["config_weather"] = WeatherSeries.get_id(project, data["config_weather"])

        if "config_geometry" in data:
            data["config_geometry"] = Geometry.get_id(project, data["config_geometry"])

        if "config_obat" in data:
            data["config_obat"] = Obat.get_id(project, data["config_obat"])

        super().update(**data)


    def start_simulation(self):
        """
        Method to start and return simulation.
        """
        response = self._client._dev_client.detail_route(
            Route.simulation_group,
            self.id,
            "POST",
            "run",
            params=dict(force=True),
            data={}
        )
        if response:
            task_id = response["user_task"]
            simulation_task = Task(task_id, self._client._dev_client)
            success = simulation_task.wait_for_completion(period=500)
            if not success:
                raise SimulationError("Simulation could not be started.")
        return self.get_simulation()

    def get_simulation(self):
        resource = self._simulations_resource.format(self.id)
        candidates = self._client._dev_client.list(resource)
        if len(candidates) != 1:
             raise ResourceNotFound(f"Simulation not be found.")
        return Simulation(candidates[0], self._client, resource)


class Simulation(APIMapping):
    _struct_type = "Simulation"
    # resource not specified because it is object-dependant

    @classmethod
    def _dev_iter(cls, client, **params):
        raise NotImplemented()

    def __init__(self, data_dict, client, resource):
        super().__init__(data_dict, client)
        self._resource = resource
