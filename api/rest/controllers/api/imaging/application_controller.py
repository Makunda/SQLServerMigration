from flask import Blueprint

from api.rest.interfaces.api_response import ApiResponse
from logger import Logger

# Define controller
from services.imaging.application_unnamed_service import ApplicationUnnamedService

application_controller = Blueprint('application', __name__,
                                   url_prefix='/application')

# Declare services & utils
logger = Logger.get_logger("Application Controller")
application_service = ApplicationUnnamedService()


# Define routes
@application_controller.route("/list", methods=['GET'])
def get_application_list():
    """
    Get the list of available applications
    :return:
    """
    try:
        application_list = application_service.get_application_list()
        response = ApiResponse("Application list", application_list, [])
        return response.repr_json(), 200
    except Exception as e:
        logger.error("Failed to get the list of the application", e)
        response = ApiResponse("Application list", None, ["Internal Error. Failed to get the application list"])
        return response.repr_json(), 500
