"""
It is responsible for database connection and health check

...

Methods
-------
connect()
    Connects to the database
check_health()
    Checks database health
"""

import mongoengine as mongo

from config import get_current_config
from log.log import logger

client = None

def connect():
    """
    Connects to the database

    It actually connects when some operation is done to the database
    """

    global client
    
    if not client:
        password = get_current_config().DB_PASSWORD
        username = get_current_config().DATABASE_USERNAME
        host = get_current_config().DATABASE_CONNECTION_STRING % (username, password)
        client = mongo.connect(
            host=host,
            connect = False
        )
        


def check_health():
    """
    Checks database health

    Returns
    -------
    boolean
        database health
    """

    try:
        client.server_info()
        return True
    except Exception as e:
        logger.exception(e)
        return False