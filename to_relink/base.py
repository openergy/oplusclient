from oplusclient import Client
import unittest
import os
import oplusclient.models
from oplusclient import exceptions


# fixme: reconnect
class AbstractTestCase(unittest.TestCase):
    resources_dir_path = os.path.join(os.path.dirname(__file__), "resources")
    api_token = os.getenv("OPLUS_API_TOKEN")
    base_url = os.getenv("OPLUS_BASE_URL")
    organization_name = os.getenv("OPLUS_ORGANIZATION_NAME")
    organization: "oplusclient.models.Organization" = None
    project: "oplusclient.models.Project" = None
    client: Client = None

    def get_client(self):
        return Client(api_token=self.api_token, base_url=self.base_url)

    def setUp(self):
        # create an organization and project
        self.client = self.get_client()
        # activate organization
        self.organization = self.client.get_organization(self.organization_name)
        if not self.organization.is_activated:
            self.organization.take_seat()
        try:
            self.organization.get_project("oplusclient-test-project").delete()
        except exceptions.RecordNotFoundError:
            pass
        self.project = self.organization.create_project("oplusclient-test-project")

    def tearDown(self) -> None:
        if self.project is not None:
            self.project.delete()
        self.organization.leave_seat()
        self.client.close()

