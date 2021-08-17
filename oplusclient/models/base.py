from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..endpoints import BaseEndpoint


class BaseModel:
    def __init__(self, endpoint: "BaseEndpoint", data):
        self.endpoint = endpoint
        self.client = self.endpoint.client
        self.data = data

    def __getattr__(self, item):
        if item not in self.data:
            raise AttributeError(f"{item} not found")
        return self.data[item]

    def __repr__(self):
        msg = f"<{self.__class__.__name__}: "
        try:
            name = self.name
            msg += f"{name} ({self.id})>"
        except AttributeError:
            msg += f"{self.id}>"
        return msg

    def _get_related(self, name, endpoint):
        data = getattr(self, name)
        return self._get_related_from_data(data, endpoint)

    def _get_related_from_data(self, data, endpoint):
        if data is None:
            return None
        if isinstance(data, list):
            return [self._get_related_from_data(d, endpoint) for d in data]
        elif isinstance(data, dict):
            return endpoint.data_to_record(data)
        else:  # by id
            return endpoint.retrieve(data)

    def reload(self):
        reloaded_data = self.endpoint.client.rest_client.retrieve(self.endpoint.route, self.id)
        self.data = reloaded_data

    def update(self, **data):
        rep_data = self.client.rest_client.partial_update(
            self.endpoint.route,
            self.id,
            data
        )
        self.data = rep_data

    def delete(self):
        self.client.rest_client.delete(
            self.endpoint.route,
            self.id
        )

    def detail_action(self, action_name, method="get", data=None, params=None):
        rep_data = self.client.rest_client.detail_action(
            self.endpoint.route,
            self.id,
            action_name,
            method=method,
            data=data,
            params=params
        )
        return rep_data
