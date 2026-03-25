from app.models.base_model import BaseModel
from app import db
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # --- NEW: Foreign Keys ---
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    allowed_update_fields = ['text', 'rating']

    def __init__(self, text, rating, user=None, place=None, **kwargs):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        if place is not None and not isinstance(place, Place):
            raise TypeError("place must be a Place instance")
        if user is not None and not isinstance(user, User):
            raise TypeError("user must be a User instance")
            
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        
        # SQLAlchemy handles linking the foreign keys when we assign these objects
        if user:
            self.user = user
        if place:
            self.place = place