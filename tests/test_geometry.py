from oplusclient import Client
import unittest
import os


class TestGeometry(unittest.TestCase):
    api_token = os.getenv("OPLUS_API_TOKEN")
    base_url = os.getenv("OPLUS_BASE_URL")
    organization = None
    project = None
    client = None

    def get_client(self):
        return Client(api_token=self.api_token, base_url=self.base_url)

    def setUp(self):
        # create an organization and project
        self.client = self.get_client()
        # activate organization
