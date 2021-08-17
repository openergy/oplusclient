from .import_export_base import BaseModel


class Organization(BaseModel):
    def get_project(self, project_name):
        """
        Get a project by name in this organization.

        Parameters
        ----------
        project_name: str

        Returns
        -------
        oplusclient.models.Project

        Raises
        ------
        RecordNotFoundError
        """
        return self.client.project.get_one_and_only_one(filter_by=dict(organization=self.id, name=project_name))

    def take_seat(self):
        """
        Take a seat in this organization.

        This must be done in order to be allowed to work on any of the organization's projects.
        """
        self.detail_action("take_up_seat", method="patch")

    def leave_seat(self):
        """
        Leave the seat you are currently on.

        After doing so, you will not be allowed to work on any of the organization's projects until you take a seat
        again.
        """
        self.detail_action("leave_seat", method="patch")

    def spend_daily_seats(self, amount=1):
        """
        Spend one of the organization daily seats.

        The seats you spend will be made available to the organization for the current day.

        Parameters
        ----------
        amount: int
            Number of seats you want to spend.
        """
        self.detail_action("spend_daily_seats", method="PATCH", data=dict(amount=amount))

    def create_project(self, name, comment="", **kwargs):
        """
        Create a new project in this organization.

        Parameters
        ----------
        name: str
        comment: str
        kwargs

        Returns
        -------
        oplusclient.models.Project
        """
        return self.client.project.create(
            organization=self.id,
            name=name,
            comment=comment,
            **kwargs
        )
