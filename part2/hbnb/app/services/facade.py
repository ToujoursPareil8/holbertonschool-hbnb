from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place

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