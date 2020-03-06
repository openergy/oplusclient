import logging

from ..models import BaseModel

logger = logging.getLogger(__name__)


class BaseEndpoint:
    MAX_ITERATIONS = 100

    def __init__(
            self,
            client,
            route,
            model_cls=None
    ):
        self.route = route
        self.client = client
        self.model_cls = BaseModel if model_cls is None else model_cls

    def data_to_record(self, data):
        return self.model_cls(self, data)

    def list(self, filter_by=None, limit=100, offset=0, extra_params=None):
        params = dict()
        if filter_by is not None:
            params.update(filter_by)
        if extra_params is not None:
            params.update(extra_params)
        if limit > 0:
            params["length"] = limit
        if offset > 0:
            params["start"] = offset
        records_data = self.client.rest_client.list(
            self.route, params=params
        )["data"]
        return [self.data_to_record(data) for data in records_data]

    def iter(self, filter_by=None, extra_params=None):
        limit = 100
        _i = 0
        for i in range(100):
            offset = i * limit
            records = self.list(
                filter_by=filter_by,
                limit=limit,
                offset=offset,
                extra_params=extra_params
            )
            if len(records) == 0:
                break
            for record in records:
                yield record
        else:
            raise RuntimeError(f"maximum iteration was reached ({self.MAX_ITERATIONS}), stopping")

    def create(self, **data):
        rep_data = self.client.rest_client.create(self.route, data)
        return self.data_to_record(rep_data)

    def retrieve(self, record_id, params=None):
        rep_data = self.client.rest_client.retrieve(self.route, record_id, params=params)
        return self.data_to_record(rep_data)


