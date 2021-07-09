import datetime as dt
from ..util import get_id
from .simulation_group import SimulationGroup


class MonoSimulationGroup(SimulationGroup):
    def get_obat(self):
        return self._get_related("config_obat", self.client.obat)

    def get_geometry(self):
        return self._get_related("config_geometry", self.client.geometry)

    def get_weather(self):
        return self._get_related("config_weather", self.client.weather)

    def get_simulation(self):
        simulations = self.list_all_simulations()
        if len(simulations) == 0:
            return None
        return simulations[0]

    def copy(self, destination_simulation_group_name) -> "MonoSimulationGroup":
        """
        Parameters
        ----------
        destination_simulation_group_name: copied simulation group name

        Returns
        -------
        copied simulation group
        """
        # create new simulation group
        sg = self.endpoint.create(
            project=get_id(self.project),
            name=destination_simulation_group_name,
            comment=self.comment

        )
        sg.update(
            config_weather=get_id(self.config_weather),
            config_geometry=get_id(self.config_geometry),
            config_obat=get_id(self.config_obat),
            config_start=self.config_start,
            config_end=self.config_end,
            config_variant=self.config_variant,
            config_outputs_detail_nfen12831=True,
            config_outputs_report=self.config_outputs_report,
        )
        return sg
