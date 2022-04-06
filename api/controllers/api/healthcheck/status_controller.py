from flask import Blueprint

from api.interfaces.api_response import ApiResponse

status_controller = Blueprint('status', __name__,
                              url_prefix='/status')


@status_controller.route("/")
def get_status():
    """
    Get the status of the application
    :return:
    """
    response = ApiResponse("status", True, [])
    return response.repr_json(), 200
