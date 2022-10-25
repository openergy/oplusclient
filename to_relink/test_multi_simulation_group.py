import os
import datetime as dt
import unittest

import pandas as pd

from oplusclient import Client, exceptions, models
from tests.base import AbstractTestCase


# fixme: reconnect
unittest.SkipTest("must manage test api token")
class TestMultiSimulationGroup(AbstractTestCase):
    obat: models.Obat = None
    weather: models.Weather = None
    geometry: models.Geometry = None
    simulation_group: models.MonoSimulationGroup = None
    simulation: models.Simulation = None

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls) -> None:
        # create an organization and project
        cls.client = Client(api_token=cls.api_token, base_url=cls.base_url)
        # activate organization
        cls.organization = cls.client.get_organization(cls.organization_name)
        if not cls.organization.is_activated:
            cls.organization.take_seat()
        try:
            cls.organization.get_project("oplusclient-test-project").delete()
        except exceptions.RecordNotFoundError:
            pass
        cls.project = cls.organization.create_project("oplusclient-test-project")
        cls.obat = cls.project.create_obat("test")
        cls.obat.import_file(os.path.join(cls.resources_dir_path, "obat", "obat.obat"))
        cls.weather = cls.project.create_weather("test", format="generic")
        cls.weather.import_file(os.path.join(cls.resources_dir_path, "weather", "weather.ow"))
        cls.geometry = cls.project.create_geometry("test", format="import")
        cls.geometry.import_file(os.path.join(cls.resources_dir_path, "geometry", "ogw.ogw"))

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.project is not None:
            cls.project.delete()
        cls.organization.leave_seat()
        cls.client.close()

    def tearDown(self) -> None:
        pass

    def test_results(self):
        simulation_group = self.project.create_multi_simulation_group("test")
        simulation_group.add_simulation(
            "test_simu",
            self.weather,
            self.geometry,
            self.obat,
            dt.datetime(2019, 1, 1),
            dt.datetime(2019, 1, 2)
        )
        simulation_group.run()
        simulation_group.wait_for_completion()
        self.assertEqual(simulation_group.status, "success")
        self.assertNotEqual(0, len(simulation_group.get_out_zones()))
        self.assertNotEqual(0, len(simulation_group.get_out_monthly_weather()))
        self.assertNotEqual(0, len(simulation_group.get_out_envelope()))
        self.assertIsInstance(simulation_group.get_out_monthly_comfort_indicators(), pd.DataFrame)
        self.assertNotEqual(0, len(simulation_group.get_out_monthly_comfort_all()))
        self.assertIsInstance(simulation_group.get_out_monthly_comfort_occ(), pd.DataFrame)
        self.assertIsInstance(simulation_group.get_out_monthly_consumption_ef(), pd.DataFrame)
        self.assertIsInstance(simulation_group.get_out_monthly_consumption_ep(), pd.DataFrame)
