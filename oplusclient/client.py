from .rest_client import RestClient
from .endpoints import BaseEndpoint
from .models import Geometry, Floorspace, Organization, Project


class Client:
    def __init__(self, api_token=None, base_url="https://oplus-back.openergy.fr/api/v1"):
        self.rest_client: RestClient = RestClient(api_token=api_token, base_url=base_url)

        # geometry
        self.geometry = BaseEndpoint(
            self,
            "ossgeometry/geometries",
            model_cls=Geometry
        )
        self.floorspace = BaseEndpoint(self, "ossgeometry/floorspace", model_cls=Floorspace)

        # oteams
        self.organization = BaseEndpoint(self, "oteams/organization", model_cls=Organization)
        self.project = BaseEndpoint(self, "oteams/project", model_cls=Project)
