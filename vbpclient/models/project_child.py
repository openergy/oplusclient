from ..struct import APIMapping


class ProjectChild(APIMapping):
    """
    Base class for objects directly related to Project.
    """
    @classmethod
    def get_id(cls, project, instance_or_str):
        if isinstance(instance_or_str, str):
            # interpreted as a name/ref
            child = project._get_child(cls, instance_or_str)
            return child.id
        elif isinstance(instance_or_str, cls):
            return instance_or_str.id
        else:
            raise ValueError(f"{instance_or_str} should be a model object or an id.")

    def get_project_id(self):
        project_link = self.project
        if isinstance(project_link, str):
            return project_link
        else:
            return project_link.id

    def get_project(self):
        return self._client.get_project_by_id(self.get_project_id())

    def __repr__(self):
        """
        Specializes __repr__ if
            `self.project` has an attribute `name`
        """
        project_link = self.project
        if isinstance(project_link, str):
            return super().__repr__()

        if not hasattr(project_link, "name"):
            return super().__repr__()

        else:
            return f"<{self._struct_type} name='{self.name}', project='{project_link.name}'>"


