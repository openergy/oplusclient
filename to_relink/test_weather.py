import os
import unittest
from tests.base import AbstractTestCase


# fixme: reconnect
unittest.SkipTest("must manage test api token")
class TestWeather(AbstractTestCase):
    def test_list_get_update(self):
        self.project.create_weather("test-weather", "generic")
        self.project.create_weather("test-weather-2", "generic")
        weather_l = self.project.list_weathers()
        self.assertEqual(len(weather_l), 2)
        self.assertEqual({g.name for g in weather_l}, {"test-weather", "test-weather-2"})
        weather_l[0].update(name="test-weather-3")
        self.project.get_weather("test-weather-3")

    def test_import_export_ow(self):
        weather = self.project.create_weather("test-weather", "generic")
        file_path = os.path.join(self.resources_dir_path, "weather", "weather.ow")
        weather.import_file(file_path)
        data = weather.export(export_format="ow")
        with open(file_path, "rb") as f:
            self.assertEqual(data, f.read())

    def test_import_export_epw_generic(self):
        weather = self.project.create_weather("test-weather", "generic")
        file_path = os.path.join(self.resources_dir_path, "weather", "weather.epw")
        weather.import_file(file_path, import_format="epw")
        data = weather.export(export_format="epw")
        with open(file_path, "rb") as f:
            self.assertEqual(data, f.read())

    def test_import_export_csv_generic(self):
        weather = self.project.create_weather("test-weather", "generic")
        file_path = os.path.join(self.resources_dir_path, "weather", "weather.csv")
        weather.import_file(file_path, import_format="csv")
        data = weather.export(export_format="csv")

    def test_import_export_epw_historical(self):
        weather = self.project.create_weather("test-weather", "historical")
        file_path = os.path.join(self.resources_dir_path, "weather", "weather.epw")
        weather.import_file(file_path, import_format="epw")
        data = weather.export(export_format="epw")
        with open(file_path, "rb") as f:
            self.assertEqual(data, f.read())

    def test_import_export_csv_historical(self):
        weather = self.project.create_weather("test-weather", "historical")
        file_path = os.path.join(self.resources_dir_path, "weather", "weather.csv")
        weather.import_file(file_path, import_format="csv")
        data = weather.export(export_format="csv")
