from app import app, db  # Change 'app' to match your main flask file
from app.models import place, amenity # Make sure to import your Amenity model!

# 1. The Data
places_data = [
  {
    "title": "The Batcave",
    "owner_id": "Bruce Wayne",
    "location": "Beneath Wayne Manor, Gotham City",
    "price": 100,
    "description": "A highly secure, high-tech subterranean command center. Features an advanced supercomputer, forensic crime labs, and a breathtaking view of a bottomless chasm. Perfect for brooding.",
    "amenities": [
      { "name": "WayneTech Secure Gigabit WiFi" },
      { "name": "King-Sized Memory Foam Bed" },
      { "name": "Decontamination Bath" }
    ],
    "image_url": "images/The_Batcave.webp"
  },
  {
    "title": "Fortress of Solitude",
    "owner_id": "Kal-El",
    "location": "The Arctic Circle",
    "price": 50,
    "description": "A massive crystalline structure built far away from civilization. Contains ancient Kryptonian technology, a cosmic zoo, and unparalleled peace and quiet. Bring a heavy coat.",
    "amenities": [
      { "name": "Kryptonian Satellite WiFi" },
      { "name": "Solar Radiation Sunbed" },
      { "name": "Heated Crystal Bath" }
    ],
    "image_url": "images/Fortress_of_Solitude.webp"
  },
  {
    "title": "The Watchtower",
    "owner_id": "Justice League",
    "location": "Geosynchronous Orbit, Earth",
    "price": 80,
    "description": "The premier orbital headquarters of the Justice League. Offers state-of-the-art monitoring systems, teleporter access, and the most spectacular view of Earth available.",
    "amenities": [
      { "name": "Deep Space Telemetry WiFi" },
      { "name": "Zero-Gravity Sleep Pod (Bed)" },
      { "name": "Sonic Cleansing Shower (Bath)" }
    ],
    "image_url": "images/Watchtower_-_Annexes.webp"
  },
  {
    "title": "Joker's Funhouse",
    "owner_id": "The Joker",
    "location": "Amusement Mile, Gotham City",
    "price": 10,
    "description": "An abandoned, neon-lit amusement park hideout. It's incredibly cheap, but dangerously unpredictable. Watch your step, don't press any big red buttons, and ignore the laughing.",
    "amenities": [
      { "name": "Unreliable Public WiFi" },
      { "name": "Spring-Loaded Surprise Bed" },
      { "name": "Acid Bath (Use with Caution)" }
    ],
    "image_url": "images/joker_base.jpg"
  }
]

# 2. The Injection Logic
def seed_database():
    with app.app_context():
        print("Starting injection...")
        
        for data in places_data:
            # Create the main Place object
            new_place = place(
                title=data['title'],
                owner_id=data['owner_id'],
                location=data['location'],
                price=data['price'],
                description=data['description'],
                image_url=data['image_url']
            )
            
            # --- THE AMENITIES ADDITION ---
            # Loop through the amenities list for this specific place
            if 'amenities' in data:
                for amenity_data in data['amenities']:
                    # Create a new Amenity object
                    new_amenity = amenity(name=amenity_data['name'])
                    
                    # Append it to the place's relationships
                    # (This assumes your Place model has a relationship defined like: amenities = db.relationship('Amenity', backref='place'))
                    new_place.amenities.append(new_amenity)
            
            # Add the place (and its attached amenities) to the staging area
            db.session.add(new_place)
            
        # Commit everything to the database at once
        db.session.commit()
        print("Success! All places and their amenities injected into the database.")

if __name__ == '__main__':
    seed_database()