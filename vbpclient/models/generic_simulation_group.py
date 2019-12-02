from ..conf import Route
from ..tasker import Task
from ..exceptions import SimulationError, ResourceNotFound
from . import ProjectChild, Weather, Geometry, Obat, Simulation


class GenericSimulationGroup(ProjectChild):
    _struct_type = "Generic Simulation Group"
    _simulations_resource = Route.generic_simulation_group + "/{}/simulations"
    _resource = Route.generic_simulation_group

    def run(self, force=False):
        """
        Method to run the simulation group
        """
        response = self._client._dev_client.detail_route(
            Route.simulation_group,
            self.id,
            "POST",
            "run",
            params=dict(force=force),
            data={}
        )
        if response:
            task_id = response["user_task"]
            simulation_task = Task(task_id, self._client._dev_client)
            success = simulation_task.wait_for_completion(period=100)
            if not success:
                raise SimulationError("Errors encountered while starting simulations.")
        return self.get_simulations()

    def add_simulation(self, **data):
        response = self._client._dev_client.detail_route(
            Route.generic_simulation_group,
            self.id,
            "POST",
            "add_simulation",
            data=data
        )
        return Simulation(response, self._client, self._simulations_resource.format(self.id))

    def delete_simulation(self, simulation):
        if not isinstance(simulation, Simulation):
            raise ValueError("simulation must be a Simulation instance")
        self._client._dev_client.detail_route(
            Route.generic_simulation_group,
            self.id,
            "DELETE",
            "delete_simulation",
            params=dict(pk=simulation.id),
            return_json=False
        )

    def get_simulations(self):
        resource = self._simulations_resource.format(self.id)
        candidates = self._client._dev_client.list(resource)
        return [Simulation(c, self._client, resource) for c in candidates]


