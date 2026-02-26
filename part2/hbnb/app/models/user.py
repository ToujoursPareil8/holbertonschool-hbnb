from app.models.base_model import BaseModel # (Assuming base_model.py is where BaseModel lives based on standard setup)

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        # We need to attach these values to the object
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        self.first_name = first_name
        
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        self.last_name = last_name
        
        if "@" not in email:
            raise ValueError("Invalid email format")
        self.email = email
        
        self.is_admin = is_admin