import io
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
        return pd.read_csv(io.StringIO(self._client._dev_client.download(
            self._resource,
            self.id,
            detail_route=detail_route
        ).decode("utf-8")))

    def get_out_hourly(self):
        df = pd.read_csv(
            io.BytesIO(self._client._dev_client.download(
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
        data = self._client._dev_client.detail_route(
            self._resource,
            self.id,
            "get",
            "generic_viz"
        )
        content = self._client._dev_client.upload_client.get(
            f"{data['container_url']}metadata.json?{data['sas_token']}").content
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        series_data = json.loads(content)

        # todo: this should not be here, index column should be in csv (improve link between obat hourly_columns
        #  and generic viz metadata)
        df = pd.DataFrame.from_records(series_data["series"])
        df.index = df.apply(_to_ref, axis=1)

        return df

    def get_out_envelope(self):
        return self._get_result("out_envelope")

    def get_out_monthly_comfort(self):
        return self._get_result("out_monthly_comfort")

    def get_out_monthly_consumption(self):
        return self._get_result("out_monthly_consumption")

    def get_out_monthly_miscellaneous(self):
        return self._get_result("out_monthly_miscellaneous")

    def get_out_monthly_thermal_balance(self):
        return self._get_result("out_monthly_thermal_balance")

    def get_out_monthly_weather(self):
        return self._get_result("out_monthly_weather")

    def get_out_zones(self):
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
