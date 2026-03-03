from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, **kwargs):
        super().__init__()
        
        # Validation
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name must be a non-empty string")
        
        # Ensure name is not too long (optional but good practice)
        if len(name) > 50:
            raise ValueError("Amenity name must be under 50 characters")
            
        self.name = name
        self.allowed_update_fields = ["name"]