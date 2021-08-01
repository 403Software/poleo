from flask_restful import Resource
from flasgger import swag_from
import os

from service.health_check_service import HealthCheckService
import definitions


class HealthCheckController(Resource):
    """
    Controller responsible for health check access

    Health checks exist so a system (or a person) can check for api
    availability or general health status (simple or detailed version)

    ...

    Endpoints
    ---------
    /health :: get()
        Gets health check status
    /health/general :: General.get()
        Gets health check general status
    """

    def __init__(self):
        """

        """

        self._health_check_service = HealthCheckService()

    @swag_from(definitions.ROOT_DIR + "/swagger/models/health_check/health-check-get.yml",
               endpoint="health")
    def get(self):
        """
        Gets health check status

        Returns
        -------
        HealthCheckResponse
            response to endpoint call
        """

        health_check_response = self._health_check_service.check_status()

        return health_check_response.to_json()

    class General(Resource):

        def __init__(self):
            """

            """

            self._health_check_service = HealthCheckService()

        @swag_from(definitions.ROOT_DIR + "/swagger/models/health_check/health-check-general.yml",
                   endpoint="health/general")
        def get(self):
            """
            Gets health check general status (detailed version)

            Returns
            -------
            HealthCheckResponse
                response to endpoint cal
            """

            health_check_response = self._health_check_service.check_general_status()

            return health_check_response.to_json()
