from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    # Keep this at the class level for your BaseModel.update logic
    allowed_update_fields = ['text', 'rating']
    
    # ADDED: **kwargs so it won't crash if extra data is passed
    def __init__(self, text, rating, user, place, **kwargs):
        super().__init__()
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        if not isinstance(place, Place):
            raise TypeError("place must be a Place instance")
        if not isinstance(user, User):
            raise TypeError("user must be a User instance")
            
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place