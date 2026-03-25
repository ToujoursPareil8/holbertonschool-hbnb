from app.models.base_model import BaseModel
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    # Database Columns
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        # Validations
        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")
        if not email or "@" not in email:
            raise ValueError("Invalid email format")

        # Call the SQLAlchemy Base constructor
        super().__init__(**kwargs)
        
        # Assignments
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        
        # Hash the password immediately if provided
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)