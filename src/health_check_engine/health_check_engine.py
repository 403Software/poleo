import threading
import datetime
import mongoengine as mongo

from log.log import logger

DATABASE = 'database'
MODEL = 'model'

FAILED = 'FAILED'
WORKING_ON = 'WORKING_ON'
LOADING = 'LOADING'
OK = 'OK'

CHECK_GENERAL_ENDPOINT = 'USE /health/general to verify'

STATUS = 'status'
TIMESTAMP = 'timestamp'
TIMESTAMP_MODEL = 'version'
TIMESTAMP_MODEL_VERSIONS = 'model_versions'

class HealthCheckEngine:
    """
    It is responsible for health check functionality

    Use HealthCheckClient for individual resource interaction

    ...

    Attributes
    ----------
    health_check_locks : dict
        locks for database checking
    health_data : dict
        health data status

    Methods
    -------
    check_general_health()
        Checks general health (detailed version)
    set_status(key, status)
        Sets health data point status
    """

    def __init__(self):
        """

        """

        self.health_check_locks = {
            DATABASE: threading.Lock(),
            MODEL: threading.Lock()
        }

        self.health_data = {
            DATABASE: {
                STATUS: STATUS,
                TIMESTAMP: str(datetime.datetime.now())
            },
            MODEL: {
                STATUS: CHECK_GENERAL_ENDPOINT,
                TIMESTAMP_MODEL: TIMESTAMP_MODEL,
                TIMESTAMP_MODEL_VERSIONS: TIMESTAMP_MODEL_VERSIONS
            }
        }

    def check_general_health(self):
        """
        Checks general health (detailed version)

        Returns
        -------
        dict
            health data
        """

        self._check_database_status()
        logger.info(self.health_data)
        return self.health_data

    def set_status(self, key, status):
        """
        Sets health data point status

        Parameters
        ----------
        key : str
            data key
        status : health constants (str)
            data status
        """

        old_status = self.health_data[MODEL][TIMESTAMP_MODEL]
        try:
            model_col = mongo.get_db()['model']
            for x in model_col.find({"active": True}):
                if old_status != x['version']:
                    self.health_data[MODEL][TIMESTAMP_MODEL] = x['version']
            versions = []
            for x in model_col.find({},{ "_id": False, "active": True, "version": True}):
                versions.append(x)
            self.health_data[MODEL][TIMESTAMP_MODEL_VERSIONS] = versions
                    
        except Exception as e:
            logger.exception(e)
            print("Error: Cannot connect to Model collection")

        if old_status != status:

            self.health_data[key][STATUS] = status
            self.health_data[key][TIMESTAMP] = str(datetime.datetime.now())

    def _check_database_status(self):
        """
        Checks database status
        """

        from database import database

        if database.check_health():
            self.set_status(DATABASE, OK)
            return
        else:
            self.set_status(DATABASE, FAILED)
            return


instance = HealthCheckEngine()
