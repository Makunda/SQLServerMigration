from abc import ABC, abstractmethod
from typing import List

from flask import Blueprint

from api.controllers.api.healthcheck.status_controller import status_controller

api_controller = Blueprint('api', __name__,
                              url_prefix='/api')

api_controller.register_blueprint(status_controller)
