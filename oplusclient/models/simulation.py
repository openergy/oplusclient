import time
import json
import io

import pandas as pd

from .base import BaseModel


DT_FORMAT = "%Y-%m-%d %H:%M:%S"


class Simulation(BaseModel):
    def get_obat(self):
        """
        Get obat.

        Returns
        -------
        oplusclient.models.Obat
        """
        return self._get_related("obat_id", self.client.obat)

    def get_geometry(self):
        """
        Get geometry.

        Returns
        -------
        oplusclient.models.Geometry
        """
        return self._get_related("geometry_id", self.client.geometry)

    def get_weather(self):
        """
        Get weather.

        Returns
        -------
        oplusclient.models.Weather
        """
        return self._get_related("weather_id", self.client.weather)

    def get_simulation_group(self):
        """
        Get simulation group.

        Returns
        -------
        oplusclient.models.SimulationGroup
        """
        return self.endpoint.parent

    def _get_result(self, detail_route):
        if not self.status == "success":
            raise ValueError(
                "Results are only available if the simulation finished successfully. However its status is"
                f" {self.status}."
            )
        download_url = self.detail_action(detail_route)["blob_url"]
        return pd.read_csv(io.StringIO(self.client.rest_client.download(
            download_url
        ).decode("utf-8")))

    def wait_for_completion(self, print_logs=False, reload_freq=3):
        """
        Wait until the simulation has finished running

        Parameters
        ----------
        print_logs: bool
            if True, prints simulation logs
        reload_freq: float
            time between two reloads in seconds
        """
        logs = ""
        while True:
            self.reload()
            if print_logs:
                new_logs = ""
                r_logs = self.logs.splitlines()
                for line_a, line_b in zip(logs.splitlines() + [""] * (len(r_logs) - len(logs.splitlines())), r_logs):
                    if line_b.strip() != line_a.strip():
                        new_logs += line_b + "\n"
                logs = "\n".join(r_logs)
                if new_logs.strip():
                    print(new_logs.strip("\n"))
            if not self.status == "running":
                break
            time.sleep(reload_freq)

    def get_out_hourly(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        download_url = self.detail_action("hourly_csv")["blob_url"]
        df = pd.read_csv(
            io.BytesIO(self.client.rest_client.download(download_url)),
            compression="zip",
            header=0,
            index_col=0,
            encoding="utf-8"
        )
        df.index = pd.to_datetime(df.index, format=DT_FORMAT)
        return df

    def get_out_hourly_columns(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        data = self.detail_action("generic_viz")
        content = self.client.rest_client.download(
            f"{data['container_url']}metadata.json?{data['sas_token']}"
        )
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        series_data = json.loads(content)

        df = pd.DataFrame.from_records(series_data["series"])
        df.index = df.apply(_to_ref, axis=1)

        return df

    def get_out_envelope(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_envelope")

    def get_out_monthly_comfort(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_comfort")

    def get_out_monthly_comfort_indicators(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_comfort_indicators")

    def get_out_monthly_consumption(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_consumption")

    def get_out_monthly_miscellaneous(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_miscellaneous")

    def get_out_monthly_thermal_balance(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        return self._get_result("out_monthly_thermal_balance")

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


def _nones_to_str(name):
    return "" if name is None else name


def _to_ref(se):
    return "|".join([
        _nones_to_str(se[k]) for k in (
            "topic",
            "name",
            "ozg",
            "azg",
            "zone",
            "unit",
            "energy_type",
            "energy_category",
            "use"
        )
    ])
