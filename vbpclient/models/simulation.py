from ..struct import APIMapping


class Simulation(APIMapping):
    _struct_type = "Simulation"
    # resource not specified because it is object-dependant

    @classmethod
    def _dev_iter(cls, client, **params):
        raise NotImplemented()

    def __init__(self, data_dict, client, resource):
        super().__init__(data_dict, client)
        self._resource = resource
