import time

from .conf import Route


class Task:
    def __init__(self, task_id, client):
        """
        Parameters
        ----------
        task_id : int
             Task identifier at `Route.task`
        client  : LowLevelClient
             Client used for API calls.

        Examples
        --------
        First use case, to hang until task finishes.

        >>> t = Task(task_id, client)
        >>> success = t.wait_for_completion()
        >>> success
        False

        Second use case, to manually prompt the reload when necessary.
        >>> t = Task(task_id, client, "user_tasks")
        >>> do_some_computations()
        >>> t.finished
        False
        >>> do_some_other_computations()
        True
        >>> t.status_code
        200
        """
        self._task_id = task_id
        self._client = client
        self._response = dict(finished=False)

    def reload(self):
        """
        Method to retrieve task information and update the object accordingly.
        """
        self._response = self._client.retrieve(Route.task, self._task_id)

    @property
    def response(self):
        if not self._response["finished"]:
            self.reload()
        return self._response.copy()

    @property
    def finished(self):
        if not self._response["finished"]:
            self.reload()
        return self._response["finished"]

    @property
    def status_code(self):
        if not self._response["finished"]:
            self.reload()
        return self._response["status_code"]

    def wait_for_completion(self, period=0):
        """
        Method to reload data until task finishes.

        Parameters
        ----------
        period  : int
            Number of milliseconds between successive data reloads.

        Returns
        -------
        bool
          Task success state as indicated by the status code.
        """
        ms = 0.001 * period
        while not self._response["finished"]:
            self.reload()
            time.sleep(ms)
        return self._response["status_code"] == 200
