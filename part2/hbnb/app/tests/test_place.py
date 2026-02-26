import unittest
from flask import json
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the test client and a clean app instance"""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place_success(self):
        """Test creating a user then a place linked to that user"""
        # 1. Create a User first (The Owner)
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.test@example.com",
            "password": "securepassword"
        }
        user_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        user_id = json.loads(user_response.data)['id']

        # 2. Create the Place using the new user_id
        place_data = {
            "title": "Test Crib",
            "description": "A test description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 1.0,
            "owner_id": user_id
        }
        response = self.client.post('/api/v1/places/', 
                                    data=json.dumps(place_data),
                                    content_type='application/json')
        
        # 3. Assertions
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['title'], "Test Crib")
        self.assertEqual(data['owner_id'], user_id)

    def test_create_place_invalid_owner(self):
        """Test creating a place with a non-existent owner ID"""
        place_data = {
            "title": "Ghost House",
            "price": 100.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": "non-existent-uuid"
        }
        response = self.client.post('/api/v1/places/', 
                                    data=json.dumps(place_data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Owner not found", json.loads(response.data)['message'])

    def test_get_all_places(self):
        """Test the list retrieval endpoint"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

if __name__ == '__main__':
    unittest.main()