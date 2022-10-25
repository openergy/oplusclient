import os
import unittest
from tests.base import AbstractTestCase


# fixme: reconnect
unittest.SkipTest("must manage test api token")
class TestObat(AbstractTestCase):
    def test_list_get_update(self):
        self.project.create_obat("test-obat")
        self.project.create_obat("test-obat-2")
        obat_l = self.project.list_obats()
        self.assertEqual(len(obat_l), 2)
        self.assertEqual({g.name for g in obat_l}, {"test-obat", "test-obat-2"})
        obat_l[0].update(name="test-obat-3")
        self.project.get_obat("test-obat-3")

    def test_import_export_obat(self):
        obat = self.project.create_obat("test-obat")
        file_path = os.path.join(self.resources_dir_path, "obat", "obat.obat")
        obat.import_file(file_path)
        data = obat.download_obat()

    def test_import_export_xlsx(self):
        obat = self.project.create_obat("test-obat")
        file_path = os.path.join(self.resources_dir_path, "obat", "obat.xlsx")
        obat.import_file(file_path, import_format="xlsx")
        data = obat.export(export_format="xlsx")
