from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        # Initialize ALL repositories in one place
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- USER METHODS ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # --- AMENITY METHODS (Placeholders) ---
    def create_amenity(self, amenity_data):
        pass

    def get_amenity(self, amenity_id):
        pass

    # --- PLACE METHODS ---
    def create_place(self, place_data):
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        # Fetch the amenities if provided
        amenities = []
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    amenities.append(amenity)

        new_place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
            amenities=amenities
        )
        
        self.place_repo.add(new_place) # This will work now!
        return new_place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        
        place.update(place_data) 
        return place
    
    # --- REVIEW METHODS ---
    def create_review(self, review_data):
            user = self.get_user(review_data['user_id'])
            place = self.get_place(review_data['place_id'])
            if not user or not place:
                raise ValueError("User or Place not found")
            
            # Validate rating
            if not (1 <= review_data['rating'] <= 5):
                raise ValueError("Rating must be between 1 and 5")

            new_review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                user=user,
                place=place
            )
            self.review_repo.add(new_review)
            return new_review
    def get_review(self, review_id):
            return self.review_repo.get(review_id)

    def get_all_reviews(self):
            return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
            all_reviews = self.get_all_reviews()
            return [r for r in all_reviews if r.place.id == place_id]

    def update_review(self, review_id, review_data):
            review = self.get_review(review_id)
            if not review:
                return None
            # Ensure 'text' and 'rating' are in Review.allowed_update_fields
            review.update(review_data)
            return review

    def delete_review(self, review_id):
            review = self.get_review(review_id)
            if not review:
                return False
            return self.review_repo.delete(review_id)