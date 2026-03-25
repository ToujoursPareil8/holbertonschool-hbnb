-- Insert the Admin User
-- The password is 'admin1234' hashed with bcrypt
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$D2M6yG5j5.A5l4V.2/4zO.nBwLzW/0Q/3H/0Q/3H/0Q/3H/0Q/3H/0', 
    TRUE
);

-- Insert the Initial Amenities with randomly generated UUIDs
INSERT INTO amenities (id, name) VALUES ('f1a2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d', 'WiFi');
INSERT INTO amenities (id, name) VALUES ('a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6', 'Swimming Pool');
INSERT INTO amenities (id, name) VALUES ('1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d', 'Air Conditioning');