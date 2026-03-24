from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt # <--- Imported get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/')
class UserList(Resource):
    
    @api.expect(user_input_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required(optional=True) # <--- optional=True allows the "Founder" to sign up without a token
    def post(self):
        """Register a new user"""
        user_data = api.payload
        
        # 1. Check if email exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # 2. THE CHICKEN AND EGG SOLVER (Bootstrap)
        all_users = facade.get_all_users()
        if len(all_users) == 0:
            # The database is empty! Make this first person an Admin automatically.
            user_data['is_admin'] = True 
        else:
            # The database is NOT empty. Check the Bouncer's rules!
            claims = get_jwt()
            if not claims or not claims.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

        # 3. Create the user
        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

@api.route('/<user_id>')
class UserResource(Resource):
    
    @api.marshal_with(user_model) 
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user, 200

    @api.expect(user_model) 
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Bad Request')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        current_user_id = get_jwt_identity()
        claims = get_jwt() # Read the back of the wristband
        is_admin = claims.get('is_admin', False)
        
        # 1. AUTHORIZATION: If you aren't an admin, and you aren't editing yourself -> Kicked out.
        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
            
        user_data = api.payload
        
        # 2. SECURITY CHECK FOR NORMAL USERS: No changing email/password
        if not is_admin:
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400

        # 3. ADMIN PRIVILEGE: If an admin is changing an email, check if it's already taken
        if is_admin and 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            # If the email exists and belongs to someone else, block it
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400
                
        # 4. Update the user!
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
            
        return {'message': 'User updated successfully'}, 200