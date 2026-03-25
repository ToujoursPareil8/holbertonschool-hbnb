from app.models.base_model import BaseModel
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    # Database Columns
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name, **kwargs):
        # Your Validation
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name must be a non-empty string")
        if len(name) > 50:
            raise ValueError("Amenity name must be under 50 characters")
            
        super().__init__(**kwargs)
        self.name = name
        self.allowed_update_fields = ["name"]