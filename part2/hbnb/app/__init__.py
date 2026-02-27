from flask import Flask
from app.api.v1 import v1_blueprint # Import the blueprint from the v1 folder

def create_app():
    app = Flask(__name__)
    
    # Register the version 1 blueprint to the app
    app.register_blueprint(v1_blueprint)
    
    return app