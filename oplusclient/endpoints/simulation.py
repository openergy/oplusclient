class SimulationEndpoint:
    def __init__(
            self,
            client,
            route,
            parent_model
    ):
        from ..models import Simulation
        self.parent = parent_model
        self.route = f"{self.parent.endpoint.route}/{self.parent.id}{route}"
        self.client = client
        self.model_cls = Simulation

    def data_to_record(self, data):
        return self.model_cls(self, data)

    def list(self, filter_by_status=None, next_marker=None):
        """
        List simulations.

        Parameters
        ----------
        filter_by_status: str or None
        next_marker: str

        Returns
        -------
        list of oplusclient.models.Simulation
        str
        """
        data = self.client.rest_client.list(
            self.route, params=dict(status=filter_by_status, next_marker=next_marker)
        )
        records_data = data["data"]
        next_marker = data.get("next_marker")
        return [self.data_to_record(data) for data in records_data], next_marker

    def iter(self, filter_by_status=None):
        next_marker = None
        while True:
            candidates, next_marker = self.list(filter_by_status=filter_by_status, next_marker=next_marker)
            for c in candidates:
                yield c
            if next_marker is None:
                break

    def retrieve(self, record_id, params=None):
        rep_data = self.client.rest_client.retrieve(self.route, record_id, params=params)
        return self.data_to_record(rep_data)

