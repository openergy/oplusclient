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
