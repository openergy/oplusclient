from ..conf import Route
from ..task import Task
from ..exceptions import SimulationError, ResourceNotFound
from . import ProjectChild, Weather, Geometry, Obat, Simulation


class MonoSimulationGroup(ProjectChild):
    _struct_type = "Mono Simulation Group"
    _simulations_resource = Route.mono_simulation_group + "/{}/simulations"
    _resource = Route.mono_simulation_group

    def update(self, **data):
        """
        Update the simulation configuration

        Parameters
        ----------
        data: dict
        """
        project = self.get_project()

        if "config_weather" in data:
            data["config_weather"] = Weather.get_id(project, data["config_weather"])

        if "config_geometry" in data:
            data["config_geometry"] = Geometry.get_id(project, data["config_geometry"])

        if "config_obat" in data:
            data["config_obat"] = Obat.get_id(project, data["config_obat"])

        super().update(**data)

    def run_simulation(self):
        """
        Runs and returns the simulation

        Returns
        -------
        Simulation
        """
        response = self._client.dev_client.detail_route(
            Route.simulation_group,
            self.id,
            "POST",
            "run",
            params=dict(force=True),
            data={}
        )
        if response:
            task_id = response["user_task"]
            simulation_task = Task(task_id, self._client.dev_client)
            success = simulation_task.wait_for_completion(period=100)
            if not success:
                raise SimulationError("Simulation could not be started.")
        return self.get_simulation()

    def get_simulation(self):
        """
        Get the mono simulation group simulation if it exists, else raise a ResourceNotFound error

        Returns
        -------
        Simulation

        Raises
        -------
        ResourceNotFound
            If the simulation group does not contain a simulation
        """
        resource = self._simulations_resource.format(self.id)
        candidates = self._client.dev_client.list(resource)
        if len(candidates) != 1:
            raise ResourceNotFound(f"Simulation not be found.")
        return Simulation(candidates[0], self._client, resource)


