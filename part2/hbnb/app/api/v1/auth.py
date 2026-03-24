from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# The Input Window for logging in
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        
        # 1. Find the user by their email
        user = facade.get_user_by_email(credentials['email'])
        
        # 2. Check if user exists AND if the password shreds match
        if not user or not user.verify_password(credentials['password']):
            api.abort(401, 'Invalid email or password')

        # 3. Print the VIP wristband (Token)
        # We put the User ID on the front, and the is_admin status on the back (claims)
        access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={"is_admin": user.is_admin}
        )
        
        return {'access_token': access_token}, 200

# ----- A Dummy Route to Test the Bouncer -----
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required() # <--- THE BOUNCER
    @api.response(200, 'Welcome to the VIP area')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        # Read the front of the wristband to get the ID
        current_user_id = get_jwt_identity() 
        return {'message': f'Welcome to the VIP area, User ID: {current_user_id}'}, 200