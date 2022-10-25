import json
import os
import unittest

from tests.base import AbstractTestCase


# fixme: reconnect
unittest.SkipTest("must manage test api token")
class TestGeometry(AbstractTestCase):
    def test_floorspace(self):
        geometry = self.project.create_geometry("test-geometry", format="floorspace")
        floorspace = geometry.get_floorspace()
        flo_path = os.path.join(self.resources_dir_path, "geometry", "floorplan.flo")
        floorspace.upload(flo_path)
        flo_data = floorspace.download()
        with open(flo_path, "rb") as f:
            self.assertEqual(flo_data, f.read())

    def test_import_floorspace(self):
        geometry = self.project.create_geometry("test-geometry", format="floorspace")
        file_path = os.path.join(self.resources_dir_path, "geometry", "floorplan.flo")
        geometry.import_file(file_path)
        data = geometry.download_source_file()
        with open(file_path, "rb") as f:
            self.assertEqual(data, f.read())

    def test_import_idf(self):
        geometry = self.project.create_geometry("test-geometry", format="import")
        file_path = os.path.join(self.resources_dir_path, "geometry", "idf.idf")
        geometry.import_file(file_path, import_format="idf")
        data = geometry.download_source_file()
        with open(file_path, "rb") as f:
            self.assertEqual(data, f.read())

    def test_import_ogw(self):
        geometry = self.project.create_geometry("test-geometry", format="import")
        file_path = os.path.join(self.resources_dir_path, "geometry", "ogw.ogw")
        geometry.import_file(file_path)
        data = geometry.download_ogw()
        with open(file_path, "rb") as f:
            self.assertEqual(json.loads(data), json.loads(f.read()))

    def test_create_list_update_geometry(self):
        self.project.create_geometry("test-geometry", format="import")
        self.project.create_geometry("test-geometry-2", format="import")
        geometry_l = self.project.list_geometries()
        self.assertEqual(len(geometry_l), 2)
        self.assertEqual({g.name for g in geometry_l}, {"test-geometry", "test-geometry-2"})
        geometry_l[0].update(name="test-geometry-3")
        self.project.get_geometry("test-geometry-3")
