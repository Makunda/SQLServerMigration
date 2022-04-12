from abc import ABC, abstractmethod
from typing import List

from flask import Blueprint
from api.rest.controllers.api.healthcheck.status_controller import status_controller
from api.rest.controllers.api.imaging.application_controller import application_controller

api_controller = Blueprint('api', __name__,
                              url_prefix='/api')

api_controller.register_blueprint(status_controller)
api_controller.register_blueprint(application_controller)
