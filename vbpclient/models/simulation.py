import io
import time
import json
import pandas as pd

from ..struct import APIMapping

DT_FORMAT = "%Y-%m-%d %H:%M:%S"


class Simulation(APIMapping):
    _struct_type = "Simulation"

    # resource not specified because it is object-dependant

    @classmethod
    def _dev_iter(cls, client, **params):
        raise NotImplemented()

    def __init__(self, data_dict, client, resource):
        super().__init__(data_dict, client)
        self._resource = resource

    def _get_result(self, detail_route):
        if not self.status == "success":
            raise ValueError(
                "Results are only available if the simulation finished successfully. However its status is"
                f" {self.status}."
            )
        return pd.read_csv(io.StringIO(self._client.dev_client.download(
            self._resource,
            self.id,
            detail_route=detail_route
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
        df = pd.read_csv(
            io.BytesIO(self._client.dev_client.download(
                self._resource,
                self.id,
                detail_route="hourly_csv"
            )),
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
        data = self._client.dev_client.detail_route(
            self._resource,
            self.id,
            "get",
            "generic_viz"
        )
        content = self._client.dev_client.upload_client.get(
            f"{data['container_url']}metadata.json?{data['sas_token']}").content
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
