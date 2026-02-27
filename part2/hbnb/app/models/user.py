from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        allowed_update_fields = ['first_name', 'last_name', 'email']
        # 1. Initialize the ID and timestamps from BaseModel
        super().__init__()
        
        # 2. Validations
        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")
        if not email or "@" not in email:
            raise ValueError("Invalid email format")
            
        # 3. Assignments
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # This fixes the crash!
        self.is_admin = is_admin