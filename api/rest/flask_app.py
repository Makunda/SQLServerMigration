
from flask import Flask
from flask_cors import CORS, cross_origin

# Create a new Application
from api.rest.controllers import api_controller

flask_application = Flask(__name__)
flask_application.debug = True

# Apply a non restrictive policy
cors = CORS(flask_application, resources={r"/api/*": {"origins": "*"}})

# Register the Blueprints / Controllers
flask_application.register_blueprint(api_controller)
