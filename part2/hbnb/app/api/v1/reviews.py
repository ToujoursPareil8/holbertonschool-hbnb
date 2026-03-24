from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# The Coffee Filter - Added 'id' so it shows up in responses!
review_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    
    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or business rule violation')
    @jwt_required() # <--- THE BOUNCER
    def post(self):
        """Register a new review"""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        
        # 1. Check if the place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            api.abort(404, 'Place not found')
            
        # 2. CONFLICT OF INTEREST: You cannot review your own place!
        if place.owner.id == current_user_id:
            api.abort(400, 'You cannot review your own place')
            
        # 3. SPAM FILTER: Have you already reviewed this place?
        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        for review in existing_reviews:
            if review.user.id == current_user_id:
                api.abort(400, 'You have already reviewed this place')

        # 4. Overwrite the user_id with the Bouncer's verified ID
        review_data['user_id'] = current_user_id
        
        try:
            new_review = facade.create_review(review_data)
            return new_review, 201
        except ValueError as e:
            api.abort(400, str(e))

    # PUBLIC ENDPOINT
    @api.marshal_list_with(review_model)
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    
    # PUBLIC ENDPOINT
    @api.marshal_with(review_model)
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review, 200

    # SECURE ENDPOINT
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required() # <--- THE BOUNCER
    def put(self, review_id):
        """Update a review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            api.abort(404, 'Review not found')
            
        # AUTHORIZATION: Did you write this review?
        if review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
            
        updated_review = facade.update_review(review_id, api.payload)
        return {'message': 'Review updated successfully'}, 200

    # SECURE ENDPOINT
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required() # <--- THE BOUNCER
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            api.abort(404, 'Review not found')
            
        # AUTHORIZATION: Did you write this review?
        if review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
            
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200