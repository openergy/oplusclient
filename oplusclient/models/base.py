import os


class BaseModel:
    def __init__(self, endpoint, data):
        # touchy imports
        from ..endpoints import BaseEndpoint
        self.endpoint: BaseEndpoint = endpoint
        self.client = self.endpoint.client
        self.data = data

    def __getattr__(self, item):
        if item not in self.data:
            raise AttributeError(f"{item} not found")
        return self.data[item]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"

    def _get_related(self, name, endpoint):
        data = self[name]
        self._get_related_from_data(data, endpoint)

    def _get_related_from_data(self, data, endpoint):
        if isinstance(data, list):
            return [self._get_related_from_data(d, endpoint) for d in data]
        elif isinstance(data, dict):
            return endpoint.data_to_record(data)
        else:  # by id
            return endpoint.retrieve(data)

    def reload(self):
        reloaded_data = self.endpoint.client.rest_client.retrieve(self.endpoint.route, self.id)
        self.data = reloaded_data

    def update(self, rep_data=None, **or_data):
        rep_data = self.client.rest_client.update(
            self.endpoint.route,
            self.id,
            or_data if rep_data is None else rep_data
        )
        self.data = rep_data[self.endpoint.route]

    def delete(self):
        self.client.rest_client.delete(
            self.plural_ref,
            self.id
        )

    def detail_action(self, action_name, method="get", data=None):
        rep_data = self.client.rest_client.detail_action(self.route, self.id, action_name, method=method, data=data)
        return rep_data
