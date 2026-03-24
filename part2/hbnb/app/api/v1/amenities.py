from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt # <--- The Bouncer Tools
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# FIXED: Added 'id' so the GET methods show it properly!
amenity_model = api.model('Amenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    
    # --- SECURE ENDPOINT: Only Admins can create amenities ---
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required() # <--- The Bouncer
    def post(self):
        """Register a new amenity"""
        claims = get_jwt()
        
        # Check for the VIP Badge
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
            
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    # --- PUBLIC ENDPOINT: Anyone can see the list of amenities ---
    @api.marshal_list_with(amenity_model)
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return amenities, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    
    # --- PUBLIC ENDPOINT: Anyone can see a specific amenity ---
    @api.marshal_with(amenity_model)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity, 200

    # --- SECURE ENDPOINT: Only Admins can edit amenities ---
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required() # <--- The Bouncer
    def put(self, amenity_id):
        """Update an amenity's information"""
        claims = get_jwt()
        
        # Check for the VIP Badge
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
            
        updated_amenity = facade.update_amenity(amenity_id, api.payload)
        if not updated_amenity:
            return {'message': 'Amenity not found'}, 404
            
        return {'message': 'Amenity updated successfully'}, 200