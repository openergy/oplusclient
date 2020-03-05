from ..exceptions import RecordNotFoundError
from ._import_export_base import BaseModel


class Organization(BaseModel):
    def get_project(self, project_name):
        try:
            return self.client.project.list(filter_by=dict(organization=self.id, name=project_name))[0]
        except KeyError:
            raise RecordNotFoundError(f"There are no project in organization {self.name} with name {project_name}")

    def take_seat(self):
        self.detail_action("take_up_seat", method="patch")

    def leave_seat(self):
        self.detail_action("leave_seat", method="patch")

    def spend_daily_seats(self, amount=1):
        self.detail_action("spend_daily_seats", method="PATCH", data=dict(amount=amount))
