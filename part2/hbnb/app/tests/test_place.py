import unittest
from flask import json
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
        # We need a user for almost every test since Places require an owner
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.test@example.com",
            "password": "securepassword"
        }
        resp = self.client.post('/api/v1/users/', 
                                data=json.dumps(user_data),
                                content_type='application/json')
        self.user_id = json.loads(resp.data)['id']

    def test_full_place_lifecycle(self):
        """Test Creating, Getting, and Updating a Place"""
        
        # 1. CREATE
        place_data = {
            "title": "Initial Title",
            "description": "Old Description",
            "price": 100.0,
            "latitude": 10.0,
            "longitude": 10.0,
            "owner_id": self.user_id
        }
        create_res = self.client.post('/api/v1/places/', 
                                      data=json.dumps(place_data),
                                      content_type='application/json')
        self.assertEqual(create_res.status_code, 201)
        place_id = json.loads(create_res.data)['id']

        # 2. GET BY ID
        get_res = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(json.loads(get_res.data)['title'], "Initial Title")

        # 3. UPDATE (PUT)
        update_data = {
            "title": "New Updated Title",
            "price": 150.0
        }
        put_res = self.client.put(f'/api/v1/places/{place_id}', 
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        self.assertEqual(put_res.status_code, 200)

        # 4. VERIFY UPDATE
        verify_res = self.client.get(f'/api/v1/places/{place_id}')
        updated_data = json.loads(verify_res.data)
        self.assertEqual(updated_data['title'], "New Updated Title")
        self.assertEqual(updated_data['price'], 150.0)

    def test_update_non_existent_place(self):
        """Test PUT request on a fake ID"""
        response = self.client.put('/api/v1/places/fake-id', 
                                    data=json.dumps({"title": "Doesn't matter"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()