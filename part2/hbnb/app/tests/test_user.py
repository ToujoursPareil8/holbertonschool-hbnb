import unittest
from flask import json
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the test client and a clean app instance"""
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Standard user payload for reuse
        self.valid_user_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com",
            "password": "securepassword123"
        }

    def test_create_user(self):
        """Test creating a valid user"""
        response = self.client.post('/api/v1/users/', 
                                    data=json.dumps(self.valid_user_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], "Alice")
        self.assertEqual(data['email'], "alice.smith@example.com")

    def test_create_user_missing_data(self):
        """Test creating a user with missing required fields"""
        bad_data = {"first_name": "NoEmail"} # Missing email and password
        response = self.client.post('/api/v1/users/', 
                                    data=json.dumps(bad_data),
                                    content_type='application/json')
        # Expecting a 400 Bad Request because the API model requires specific fields
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        """Test retrieving the list of all users"""
        # Create a user first so the list isn't empty
        self.client.post('/api/v1/users/', 
                         data=json.dumps(self.valid_user_data),
                         content_type='application/json')
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_user_by_id(self):
        """Test retrieving a specific user by their ID"""
        # 1. Create the user
        create_res = self.client.post('/api/v1/users/', 
                                      data=json.dumps(self.valid_user_data),
                                      content_type='application/json')
        user_id = json.loads(create_res.data)['id']

        # 2. Fetch the user
        get_res = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_res.status_code, 200)
        
        data = json.loads(get_res.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['first_name'], "Alice")

    def test_get_non_existent_user(self):
        """Test retrieving a user ID that does not exist"""
        response = self.client.get('/api/v1/users/fake-uuid-1234')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """Test updating a user's information"""
        # 1. Create the user
        create_res = self.client.post('/api/v1/users/', 
                                      data=json.dumps(self.valid_user_data),
                                      content_type='application/json')
        user_id = json.loads(create_res.data)['id']

        # 2. Update the user
        update_data = {
            "first_name": "Alicia",
            "last_name": "Jones"
        }
        put_res = self.client.put(f'/api/v1/users/{user_id}', 
                                  data=json.dumps(update_data),
                                  content_type='application/json')
        self.assertEqual(put_res.status_code, 200)

        # 3. Verify the changes were saved
        verify_res = self.client.get(f'/api/v1/users/{user_id}')
        updated_data = json.loads(verify_res.data)
        self.assertEqual(updated_data['first_name'], "Alicia")
        self.assertEqual(updated_data['last_name'], "Jones")

if __name__ == '__main__':
    unittest.main()