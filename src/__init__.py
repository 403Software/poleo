"""
It is responsible for the Flask app configuration

...

Methods
-------
configure_database()
    Configures database
configure_recommendation_engine()
    Configures recommendation engine
configure_api()
    Configures api's endpoints
create_app(config_name)
    Creates app
"""

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import json_logging
from flasgger import Swagger

from database import database
from log.log import logger

import definitions
from config import get_current_config, config
from controller.health_check_controller import HealthCheckController

current_config = get_current_config()

app = Flask('oner-flask-rest-api-exemple')

app.config['SWAGGER'] = {
    'title': "ONER-FLASK-REST Service Api",
    'uiversion': 3,
    'description': "ONER-FLASK-REST Service Endpoints"
}

CORS(app)
# noinspection PyTypeChecker
api = Api(app)
swagger = Swagger(app, template_file=definitions.ROOT_DIR +
                  '/swagger/template.yml')

json_logging.ENABLE_JSON_LOGGING = True
try:
    json_logging.init_flask()
    json_logging.init_request_instrument(app)
except BaseException as e:
    logger.exception(e)


def configure_database():
    """
    Configures database
    """

    database.connect()

def configure_api():
    """
    Configures api's endpoints
    """
    try:
        api.add_resource(HealthCheckController, '/health', endpoint='health')
        api.add_resource(HealthCheckController.General,
                        '/health/general', endpoint='health/general')
    except:
        pass


def create_app(config_name):
    """
    Creates app

    Parameters
    ----------
    config_name : str
        flask env

    Returns
    -------
    Flask
        app
    """
    app.config.from_object(config[config_name])
    app.config['ERROR_404_HELP'] = False

    configure_api()

    configure_database()

    return app
