from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        
        # Validation
        if not isinstance(name, str):
            raise TypeError("Amenity name must be a string")
        
        self.name = name
        self.allowed_update_fields = ["name"]
