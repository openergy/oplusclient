import io

import pandas as pd
from . import SimulationGroup, Weather, Geometry, Obat


class MultiSimulationGroup(SimulationGroup):
    def add_simulation(
            self,
            name,
            weather,
            geometry,
            obat,
            start,
            end,
            variant=None,
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
        outputs_detail_nfen12831: bool
        outputs_report: bool

        Returns
        -------
        Simulation
        """
        if isinstance(weather, Weather):
            weather = weather.id
        if isinstance(geometry, Geometry):
            geometry = geometry.id
        if isinstance(obat, Obat):
            obat = obat.id
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
                    outputs_detail_nfen12831=outputs_detail_nfen12831,
                    outputs_report=outputs_report
                )
            )
        )

    def update_simulation(self, **kwargs):
        """
        Update a simulation.

        Parameters
        ----------
        name: str
        weather: Weather or str
        geometry: Geometry or str
        start: datetime.date
        end: datetime.date
        variant: str or None
        outputs_detail_nfen12831: bool
        outputs_report: bool

        Returns
        -------
        Simulation
        """
        if isinstance(kwargs.get("weather", None), Weather):
            kwargs["weather"] = kwargs["weather"].id
        if isinstance(kwargs.get("geometry", None), Geometry):
            kwargs["geometry"] = kwargs["geometry"].id
        return self.simulation_endpoint.data_to_record(
            self.detail_action(
                "update_simulation",
                "PATCH",
                data=kwargs
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

    def _get_result(self, detail_route):
        if not self.status == "success":
            raise ValueError(
                f"Results are only available if the simulation finished successfully. However its status is"
                f" {self.status}."
            )
        download_url = self.detail_action(detail_route)["blob_url"]
        return pd.read_csv(io.StringIO(self.client.rest_client.download(
            download_url
        ).decode("utf-8")))

    def get_out_envelope(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_envelope")

    def get_out_monthly_comfort_all(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_comfort_all")

    def get_out_monthly_comfort_indicators(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_comfort_indicators")

    def get_out_monthly_comfort_occ(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_comfort_occ")

    def get_out_monthly_consumption_ef(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_consumption_ef")

    def get_out_monthly_consumption_ep(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_consumption_ep")

    def get_out_monthly_weather(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_weather")

    def get_out_zones(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_zones")
