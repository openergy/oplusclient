import pandas as pd
import io

from ..struct import APIMapping


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
            raise ValueError("Results are only available if the simulation finished successfully. However its status is"
                             f" {self.status}.")
        return pd.read_csv(io.StringIO(self._client._dev_client.download(
            self._resource,
            self.id,
            detail_route=detail_route
        ).decode("utf-8")))

    def get_out_hourly(self):
        return self._get_result("hourly_csv")

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
