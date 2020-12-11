from . import SimulationGroup, Weather, Geometry, Obat


class GenericSimulationGroup(SimulationGroup):
    def add_simulation(
        self,
        name,
        weather,
        geometry,
        obat,
        start,
        end,
        variant=None,
        substitute_modifications=None,
        outputs_detail_nfen12831=False,
        outputs_report=False
    ):
        """
        Add a simulation.

        Parameters
        ----------
        name: str
        weather: Weather or str
        geometry: Geometry or str
        obat: Obat or str
        start: datetime.date
        end: datetime.date
        variant: str or None
        substitute_modifications: dict or None
        outputs_detailed_nfen12831: bool
        outputs_report: bool

        Returns
        -------
        oplusclient.models.Simulation
        """
        if isinstance(obat, Obat):
            obat = obat.id
        if isinstance(weather, Weather):
            weather = weather.id
        if isinstance(geometry, Geometry):
            geometry = geometry.id
        return self.simulation_endpoint.data_to_record(
            self.detail_action(
                "add_simulation",
                "POST",
                data=dict(
                    name=name,
                    weather_id=weather,
                    geometry_id=geometry,
                    obat_id=obat,
                    start=start.strftime("%Y-%m-%dT00:00:00"),
                    end=end.strftime("%Y-%m-%dT23:59:59"),
                    variant=variant,
                    substitute_modifications=substitute_modifications,
                    outputs_detail_nfen12831=outputs_detail_nfen12831,
                    outputs_report=outputs_report
                )
            )
        )

    def delete_simulation(self, simulation):
        """
        Delete a simulation.

        Parameters
        ----------
        simulation: Simulation or str
            Simulation instance or simulation id
        """
        from . import Simulation
        if isinstance(simulation, Simulation):
            simulation = simulation.id
        self.detail_action("delete_simulation", "DELETE", data=dict(id=simulation))
