import uuid
from datetime import datetime
from app import db

class BaseModel(db.Model):
    # This tells SQLAlchemy NOT to create a table for BaseModel
    __abstract__ = True  

    # SQLAlchemy Columns
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def update(self, data):
        """Utility method to update attributes from a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)