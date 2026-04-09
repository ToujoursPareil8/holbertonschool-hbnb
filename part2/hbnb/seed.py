from app import create_app, db
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity

app = create_app()

places_data = [
    # ... keep all your data and the rest of the script exactly the same!
    {
        "title": "The Batcave",
        "owner_name": "Bruce Wayne",
        "latitude": 40.7128,  # Gotham (NYC coordinates)
        "longitude": -74.0060,
        "price": 847807.0,
        "description": "A highly secure, high-tech subterranean command center. Features an advanced supercomputer, forensic crime labs, and a breathtaking view of a bottomless chasm. Perfect for brooding.",
        "amenities": ["WayneTech Secure Gigabit WiFi", "King-Sized Memory Foam Bed", "Decontamination Bath"]
    },
    {
        "title": "Fortress of Solitude",
        "owner_name": "Kal-El",
        "latitude": 82.8628,  # The Arctic
        "longitude": -135.0000,
        "price": 5555.0,
        "description": "A massive crystalline structure built far away from civilization. Contains ancient Kryptonian technology, a cosmic zoo, and unparalleled peace and quiet. Bring a heavy coat.",
        "amenities": ["Kryptonian Satellite WiFi", "Solar Radiation Sunbed", "Heated Crystal Bath"]
    },
    {
        "title": "The Watchtower",
        "owner_name": "Justice League",
        "latitude": 0.0,      # Space/Equator orbit
        "longitude": 0.0,
        "price": 82300.0,
        "description": "The premier orbital headquarters of the Justice League. Offers state-of-the-art monitoring systems, teleporter access, and the most spectacular view of Earth available.",
        "amenities": ["Deep Space Telemetry WiFi", "Zero-Gravity Sleep Pod (Bed)", "Sonic Cleansing Shower (Bath)"]
    },
    {
        "title": "Joker's Funhouse",
        "owner_name": "The Joker",
        "latitude": 40.5749,  # Amusement Mile (Coney Island coordinates)
        "longitude": -73.9785,
        "price": 0.10,
        "description": "An abandoned, neon-lit amusement park hideout. It's incredibly cheap, but dangerously unpredictable. Watch your step, don't press any big red buttons, and ignore the laughing.",
        "amenities": ["Unreliable Public WiFi", "Spring-Loaded Surprise Bed", "Acid Bath (Use with Caution)"]
    }
]

def get_or_create_user(name):
    """Creates dummy users so we have valid UUIDs for the owner_id constraint."""
    parts = name.split(" ", 1)
    first_name = parts[0]
    
    # FIX 1: If they don't have a last name (like Kal-El), give them a placeholder
    # to pass your strict User model validation!
    last_name = parts[1] if len(parts) > 1 else "Unknown" 
    
    email = f"{first_name.lower()}@dcuniverse.com"

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return existing_user

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password="password123"
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def seed_database():
    with app.app_context():
        print("Starting injection sequence...")
        
        for data in places_data:
            print(f"Injecting: {data['title']}...")
            
            owner = get_or_create_user(data['owner_name'])
            
            if Place.query.filter_by(title=data['title']).first():
                print(f"  -> {data['title']} already exists, skipping.")
                continue

            new_place = Place(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                owner_id=owner.id 
            )
            
            # FIX 2: Add the place to the session FIRST before querying/attaching amenities
            # This completely solves the SAWarning!
            db.session.add(new_place)
            
            for amenity_name in data['amenities']:
                amenity = Amenity.query.filter_by(name=amenity_name).first()
                if not amenity:
                    amenity = Amenity(name=amenity_name)
                    db.session.add(amenity)
                
                new_place.add_amenity(amenity)
            
        db.session.commit()
        print("Success! Database injection complete.")

if __name__ == '__main__':
    seed_database()