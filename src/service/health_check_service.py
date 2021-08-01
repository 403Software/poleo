from model.health_check.health_check_response import HealthCheckResponse
import health_check_engine.health_check_engine as health_check_engine


class HealthCheckService:
    """
    It is responsible for providing health checks from health check engine

    ...

    Methods
    -------
    check_status()
        Checks health status
    check_general_status()
        Checks health status with detailed information
    """

    def check_status(self):
        """
        Checks health status

        To be called by services wanting to know if api is responsive

        Returns
        -------
        HealthCheckResponse
            the simple version of health check status
        """

        health_check_status = 'USE /health/general to verify'
        health_check_response = HealthCheckResponse(health_check_status)

        return health_check_response

    def check_general_status(self):
        """
        Checks health status with detailed information

        To be called for troubleshooting

        Returns
        -------
        HealthCheckResponse
            the detailed version of heath check status
        """

        health_data = health_check_engine.instance.check_general_health()

        return self._check_status(health_data)

    def _check_status(self, health_data):
        """
        Checks components health status

        Parameters
        ----------
        health_data : dict
            health data from health check engine

        Returns
        -------
        HealthCheckResponse
            a user-friendly heath check response
        """

        health_check_status = 'RUNNING'

        for value in health_data.values():
            if value[health_check_engine.STATUS] != health_check_engine.OK:
                health_check_status = 'CHECK HEALTH DATA'

        health_check_response = HealthCheckResponse(
            health_check_status, health_data)

        return health_check_response
