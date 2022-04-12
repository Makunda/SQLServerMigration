from flask import Blueprint

from api.rest.interfaces.api_response import ApiResponse
from api.rest.interfaces.healthcheck.status import Status

status_controller = Blueprint('status', __name__,
                              url_prefix='/status')


@status_controller.route("/")
def get_status():
    """
    Get the status of the application
    :return:
    """
    status = Status(True)
    response = ApiResponse("status", status, [])
    return response.repr_json(), 200
