import json

from .tasker import Task


class FrozenClass:
    """
    Parent class that prevents attribute monkey patching after __init__ is called.
    Direct sub-classes should call ._freeze() after __init__.
    """
    __is_frozen = False

    def _freeze(self):
        self.__is_frozen = True

    def __setattr__(self, attr, value):
        if self.__is_frozen:
            raise AttributeError(f"Attribute 'attr' is read-only.")
        else:
            super().__setattr__(attr, value)


class Struct(FrozenClass):
    """
    A base class for recursively building objects from json-like dictionaries
    Inherits from FrozenClass to prevent monkey patching after __init__.
    """
    def __init__(self, d):
        """
        Parameters
        ----------
        d: dictionary

        Returns
        -------
        An object with identical data to d except key access is only possible with the attribute dot notation.
        """
        self._to_str = json.dumps(d, indent=4, default=str)
        self.keys_view = lambda: d.keys()
        for key, value in d.items():
            if not isinstance(key, str):
                raise TypeError(f"Key '{key}' is not an instance of str.")
            if isinstance(value, dict):
                setattr(self, key, Struct(value))
            elif isinstance(value, (list, tuple)):
                setattr(self, key, [
                    Struct(element) if isinstance(element, dict) else element for element in value
                ])
            else:
                # TODO any other type is accepted, at first it was (NoneType, str, int, float) but after a few
                # a few bugs with `datetime` objects it was changed temporarily
                setattr(self, key, value)
        self._freeze()

    def __str__(self):
        return self._to_str

    def __repr__(self):
        return f"<Object id='{self.id}'>"


class APIMapping:
    """
    A base class for all important classes (Project, Organization, Simulation-Group...).
    Important implies they not only contain data but also functionality (they can make API client calls).
    """
    _struct_type = "Object"
    _resource = "/" # this is just a placeholder, absolutely must be subclassed. so maybe None.
    _json_data = dict()

    def __init__(self, data_dict, client):
        """
        Parameters
        ----------
        data_dict: dict
        client: vbpclient.OSSClient
        """
        self._json_data = data_dict
        self._struct_data = Struct(data_dict)
        self._client = client

    def __getattr__(self, attr):
        if attr in self._json_data:
            return getattr(self._struct_data, attr)
        else:
            print(self._json_data)
            raise AttributeError(f"Attribute '{attr}' not found.")

    def __setattr__(self, attr, value):
        if attr in self._json_data:
            raise AttributeError(f"Attribute '{attr}' is read-only.")
        else:
            super().__setattr__(attr, value)

    @classmethod
    def _dev_iter(cls, client, **params):
        json_data = client._dev_client.list_iter_all(cls._resource, params=params)
        return (
            cls(element, client) for element in json_data
        )

    @property
    def json_data(self):
        return self._json_data.copy()

    @property
    def keys_view(self):
        return self._json_data.keys()

    def reload(self):
        refreshed_data = self._client._dev_client.retrieve(self._resource, self.id)
        if not self._json_data == refreshed_data:
            self._json_data = refreshed_data
            self._struct_data = Struct(refreshed_data)

    def update(self, **data):
        updated_data = self._client._dev_client.partial_update(self._resource, self.id, data)
        self._json_data = updated_data
        self._struct_data = Struct(updated_data)

    def destroy(self):
        task_id = self._client._dev_client.destroy(self._resource, self.id)
        if task_id:
            destroy_task = Task(task_id, self._client._dev_client)
            success = destroy_task.wait_for_completion(period=0)
            if not success:
                raise RuntimeError(f"{self._struct_type} could not be removed.\n"
                                   f"{destroy_task.message}\n"
                                   f"{destroy_task.response['_out_text']}")

    def __repr__(self):
        return f"<{self._struct_type} id='{self.id}'>"

    def __str__(self):
        return str(self._struct_data)

