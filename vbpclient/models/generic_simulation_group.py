from ..conf import Route
from ..task import Task
from ..exceptions import SimulationError
from . import ProjectChild, Simulation


class GenericSimulationGroup(ProjectChild):
    _struct_type = "Generic Simulation Group"
    _simulations_resource = Route.generic_simulation_group + "/{}/simulations"
    _resource = Route.generic_simulation_group

    def run(self, force=False):
        """
        Runs the simulation

        Parameters
        ----------
        force: bool
            If force, the simulation group runs even if the simulation group is not empty or obsolete

        Returns
        -------
        typing.List[Simulation]
        """
        response = self._client.dev_client.detail_route(
            Route.simulation_group,
            self.id,
            "POST",
            "run",
            params=dict(force=force),
            data={}
        )
        if response:
            task_id = response["user_task"]
            simulation_task = Task(task_id, self._client.dev_client)
            success = simulation_task.wait_for_completion(period=100)
            if not success:
                raise SimulationError("Errors encountered while starting simulations.")
        return self.get_simulations()

    def add_simulation(self, **data):
        """
        Add a simulation to the group

        Parameters
        ----------
        data: dict
            Simulation data

        Returns
        -------
        Simulation
        """
        response = self._client.dev_client.detail_route(
            Route.generic_simulation_group,
            self.id,
            "POST",
            "add_simulation",
            data=data
        )
        return Simulation(response, self._client, self._simulations_resource.format(self.id))

    def delete_simulation(self, simulation):
        """
        Delete simulation from the group

        Parameters
        ----------
        simulation: Simulation
        """
        if not isinstance(simulation, Simulation):
            raise ValueError("simulation must be a Simulation instance")
        self._client.dev_client.detail_route(
            Route.generic_simulation_group,
            self.id,
            "DELETE",
            "delete_simulation",
            params=dict(pk=simulation.id),
            return_json=False
        )

    def get_simulations(self):
        """
        Get a list of the simulations in the simulation group

        Returns
        -------
        typing.List[Simulation]
        """
        resource = self._simulations_resource.format(self.id)
        candidates = self._client.dev_client.list(resource)
        return [Simulation(c, self._client, resource) for c in candidates]


