from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"): # <-- Fixed config_class
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)

    # Hire the department manager
    from app.api.v1 import v1_blueprint
    app.register_blueprint(v1_blueprint)
    
    return app