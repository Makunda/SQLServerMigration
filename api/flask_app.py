from flask import Flask

# Create a new Application
from api.controllers.api_controller import api_controller

flask_application = Flask(__name__)
flask_application.debug = True

# Register the Blueprints / Controllers
flask_application.register_blueprint(api_controller)
