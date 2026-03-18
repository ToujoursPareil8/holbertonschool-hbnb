from flask import Flask
from app.api.v1 import v1_blueprint
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app():
    """
    Application Factory: Creates and configures the Flask application.
    By default, it uses the Development configuration.
    """
    app = Flask(__name__)
    # It reads the blueprint and applies all the settings to the app.
    app.config.from_object(config_class)
    bcrypt.init_app(app)

    from app.api.v1 import v1_blueprint

    # We re-attach the RESTx API to the blueprint (if not already done inside the blueprint file)
    api = Api(v1_blueprint, version='1.0', title='HBnB API', description='HBnB Application API')
    
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')
    
    app.register_blueprint(v1_blueprint)
    return app