from config import get_current_config


class HealthCheckResponse:
    """
    Health check response model

    ...

    Attributes
    ----------
    api : str
        api's name
    version : str
        api's version
    status : status constants (str)
        main status
    health_data : dict
        health data

    Methods
    -------
    to_json()
        Transforms data structure to dict (accepted as json)
    """

    def __init__(self, status, health_data=None):
        """
        Parameters
        ----------
        status : status constants (str)
            main status
        health_data : dict
            health data
        """

        self.api = get_current_config().API
        self.version = get_current_config().VERSION
        self.status = status
        if health_data is not None:
            self.health_data = health_data

    def to_json(self):
        """
        Transforms data structure to dict (accepted as json)

        Returns
        -------
        dict
            dict version of data
        """

        return self.__dict__
