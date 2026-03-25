from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates

# --- NEW: Association Table for Many-to-Many ---
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # --- NEW: Foreign Keys & Relationships ---
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # cascade="all, delete-orphan" means if a Place is deleted, its Reviews are deleted too!
    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    
    # This connects to the association table we built above
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(self, title, description, price, latitude, longitude, owner=None, amenities=None, **kwargs):
        super().__init__(**kwargs)
        
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        
        # SQLAlchemy intercepts these assignments and links them in the database!
        if owner:
            self.owner = owner
        if amenities:
            self.amenities = amenities
            
        self.allowed_update_fields = ["title", "description", "price", "latitude", "longitude"]

    @validates('title')
    def validate_title(self, key, value):
        if not value or len(value) > 100:
            raise ValueError("Title is required and cannot exceed 100 characters")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if float(value) < 0:
            raise ValueError("Price must be a non-negative float")
        return float(value)

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not (-90.0 <= float(value) <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        return float(value)

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not (-180.0 <= float(value) <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")
        return float(value)

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)