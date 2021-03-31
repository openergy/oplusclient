import time
import json
import io
import datetime as dt

import pandas as pd

from .. import exceptions
from .import_export_base import BaseModel


DT_FORMAT = "%Y-%m-%d %H:%M:%S"
ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


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

    def _get_generic_viz_blob_info(self):
        return self.detail_action("generic_viz")

    def _download_out_hourly_file(self, file_path, generic_viz_blob_info=None):
        """
        file_path must not start with /
        """
        if generic_viz_blob_info is None:
            generic_viz_blob_info = self._get_generic_viz_blob_info()
        data = self.client.rest_client.download(
            f"{generic_viz_blob_info['container_url']}{file_path}?{generic_viz_blob_info['sas_token']}"
        )
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        return data

    def _download_out_hourly_metadata(self, generic_viz_blob_info=None):
        raw = self._download_out_hourly_file("metadata.json", generic_viz_blob_info=generic_viz_blob_info)
        return json.loads(raw)

    def _download_out_hourly_index(self, year, generic_viz_blob_info=None):
        raw = self._download_out_hourly_file(f"{year}/index.json", generic_viz_blob_info=generic_viz_blob_info)
        return json.loads(raw)

    def _download_out_hourly_se(self, year, series_id, generic_viz_blob_info=None):
        raw = self._download_out_hourly_file(f"{year}/{series_id}.json")
        return json.loads(raw)

    def get_out_hourly(self, series_ids=None):
        """
        Parameters
        ----------
        series_ids: optional, list of ids
            if not provided: all outputs will be downloaded from stored csv
            if provided: only given ids will be provided, outputs will be downloaded series by series using
                (as in generic viz). The series ids can be found using the "get_out_hourly_columns" dataframe.

        Returns
        -------
        pd.DataFrame
        """
        # whole csv
        if series_ids is None:
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

        # series by series mode

        # prepare generic viz info
        generic_viz_blob_info = self._get_generic_viz_blob_info()

        # choose year
        metadata = self._download_out_hourly_metadata(generic_viz_blob_info=generic_viz_blob_info)
        if len(metadata["years"]) != 1:
            raise NotImplementedError(
                f"Series by series download mode is not implemented for multiple year simulations. "
                f"Current simulation years: {metadata['years']}")
        year = metadata["years"][0]

        # fixme: make async

        # index
        index_data = self._download_out_hourly_index(year, generic_viz_blob_info=generic_viz_blob_info)
        index = pd.DatetimeIndex(map(lambda x: dt.datetime.strptime(x, ISO_FORMAT), index_data))

        data = dict()
        for se_id in series_ids:
            # todo: manage not found
            try:
                data[se_id] = self._download_out_hourly_se(year, se_id, generic_viz_blob_info=generic_viz_blob_info)
            except exceptions.HttpClientError as e:
                if e.status_code == 404:
                    raise ValueError(f"Simulation does not contain a series with given id '{se_id}'.")

        return pd.DataFrame(data=data, index=index)

    def get_out_hourly_columns(self):
        """
        Returns
        -------
        pd.DataFrame
        """
        metadata = self._download_out_hourly_metadata()
        df = pd.DataFrame.from_records(metadata["series"])
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

    def download_eplus_output(self, buffer_or_path=None):
        """
        Parameters
        ----------
        buffer_or_path: buffer or path where to save the zipfile with eplus output (if None, returns bytes)

        Returns
        -------
        bytes or None
        """
        download_url = self.detail_action("eplus_output")["blob_url"]
        return self.client.rest_client.download(download_url, buffer_or_path=buffer_or_path)

    def download_report(self, buffer_or_path=None):
        """
        Parameters
        ----------
        buffer_or_path: buffer or path where to save the report (docx format) (if None, returns bytes)

        Returns
        -------
        bytes or None
        """
        download_url = self.detail_action("report_output")["blob_url"]
        return self.client.rest_client.download(download_url, buffer_or_path=buffer_or_path)


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
