from flask import Blueprint
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# This creates the logical grouping for version 1
v1_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# This attaches the RESTx API to that blueprint
api = Api(v1_blueprint, 
          version='1.0', 
          title='HBnB API', 
          description='HBnB Application API')

# Register the namespaces
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')