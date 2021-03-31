import time
from typing import Iterable

from ..endpoints.simulation import SimulationEndpoint
from ..models.simulation import Simulation
from .. import exceptions
from ..task import Task
from .base import BaseModel


class SimulationGroup(BaseModel):
    def __init__(self, endpoint, data):
        super().__init__(endpoint, data)
        self.simulation_endpoint = SimulationEndpoint(self.client, "/simulations", self)

    def run(self, run_old_versions=False, wait_for_start_task=True):
        """
        Run the simulation group.

        Parameters
        ----------
        run_old_versions: bool
        wait_for_start_task: bool
        """
        run_task = Task(
            self.detail_action("run", method="POST", params=dict(run_old_versions=run_old_versions))["user_task"],
            self.client.rest_client
        )
        if wait_for_start_task:
            if not run_task.wait_for_completion():
                raise exceptions.OplusClientError(f"Could not start simulation. Message:\n{run_task.message}")

    def wait_for_completion(self, period=200):
        """
        Wait for the simulation group to finish running

        Parameters
        ----------
        period  : int
            Number of milliseconds between successive data reloads.
        """
        ms = 1e-3 * period
        self.reload()
        while self.working:
            time.sleep(ms)
            self.reload()

    def iter_simulations(self, filter_by_status=None) -> Iterable[Simulation]:
        """
        Iter through all simulations of the simulation group.

        Parameters
        ----------
        filter_by_status: str or None
            Only list simulations with this status.

        Returns
        -------
        typing.Iterator of oplusclient.models.Simulation
        """
        return self.simulation_endpoint.iter(filter_by_status=filter_by_status)

    def list_all_simulations(self, filter_by_status=None):
        """
        List all simulations in a simulation group.

        Beware: if there is a high number of simulations, this can take a while.
        It is recommended to use iter_simulations instead.

        Parameters
        ----------
        filter_by_status: str or None
            Only list simulations with this status

        Returns
        -------
        list of oplusclient.models.Simulation
        """
        return list(self.iter_simulations(filter_by_status=filter_by_status))

    def get_simulation_by_name(self, name):
        """
        Find a simulation by name.

        Beware on big simulation groups this an be long due to client-side filtering.
        
        Returns
        -------
        oplusclient.models.Simulation
        """
        for s in self.iter_simulations():
            if s.name == name:
                return s
        else:
            raise exceptions.RecordNotFoundError(f"There are no simulations in this simulation group with name {name}")
