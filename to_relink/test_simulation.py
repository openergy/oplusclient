import os
import unittest
from oplusclient import Client, exceptions, models
from tests.base import AbstractTestCase


# fixme: reconnect
unittest.SkipTest("must manage test api token")
class TestSimulation(AbstractTestCase):
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
        cls.simulation_group = cls.project.create_mono_simulation_group(
            "test",
            config_start="2019-01-01T00:00:00",
            config_end="2019-02-01T23:59:59",
            config_obat=cls.obat.id,
            config_geometry=cls.geometry.id,
            config_weather=cls.weather.id,
            config_outputs_report=True
        )
        print("running simulation")
        cls.simulation_group.run()
        cls.simulation = cls.simulation_group.get_simulation()
        cls.simulation.wait_for_completion(print_logs=True, reload_freq=1)

    @classmethod
    def tearDownClass(cls) -> None:
        # if cls.project is not None:
        #     cls.project.delete()
        cls.organization.leave_seat()
        cls.client.close()

    def tearDown(self) -> None:
        pass

    def test_results(self):
        self.assertNotEqual(0, len(self.simulation.get_out_monthly_comfort_indicators().columns))
        self.assertNotEqual(0, len(self.simulation.get_out_monthly_comfort().columns))
        self.assertNotEqual(0, len(self.simulation.get_out_envelope().columns))
        self.assertNotEqual(0, len(self.simulation.get_out_hourly().columns))
        self.assertNotEqual(0, len(self.simulation.get_out_hourly_columns().columns))
        self.assertNotEqual(0, len(self.simulation.get_out_monthly_consumption().columns))
        self.assertNotEqual(0, len(self.simulation.get_out_monthly_miscellaneous().columns))
        self.assertNotEqual(0, len(self.simulation.get_out_monthly_thermal_balance().columns))
        self.assertNotEqual(0, len(self.simulation.get_out_monthly_weather().columns))
        self.assertNotEqual(0, len(self.simulation.get_out_zones().columns))
        self.assertTrue(isinstance(self.simulation.download_eplus_output(), bytes))
        self.assertTrue(isinstance(self.simulation.download_report(), bytes))
