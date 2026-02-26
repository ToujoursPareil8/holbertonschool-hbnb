import unittest
from flask import json
from app import create_app

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the test client and generate prerequisites (User and Place)"""
        self.app = create_app()
        self.client = self.app.test_client()

        # 1. Create a User (Acts as owner and reviewer for simplicity)
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "password": "password123"
        }
        user_res = self.client.post('/api/v1/users/', 
                                    data=json.dumps(user_data), 
                                    content_type='application/json')
        self.user_id = json.loads(user_res.data)['id']

        # 2. Create a Place linked to the User
        place_data = {
            "title": "Test Place",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 10.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
            "amenities": []
        }
        place_res = self.client.post('/api/v1/places/', 
                                     data=json.dumps(place_data), 
                                     content_type='application/json')
        self.place_id = json.loads(place_res.data)['id']

        # Standard review payload for reuse in tests
        self.valid_review_data = {
            "text": "Amazing experience!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }

    def test_create_review(self):
        """Test creating a valid review"""
        response = self.client.post('/api/v1/reviews/', 
                                    data=json.dumps(self.valid_review_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['text'], "Amazing experience!")
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid_rating(self):
        """Test creating a review with a rating out of bounds (1-5)"""
        bad_data = self.valid_review_data.copy()
        bad_data['rating'] = 6
        response = self.client.post('/api/v1/reviews/', 
                                    data=json.dumps(bad_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_review_by_id(self):
        """Test retrieving a specific review"""
        # First create it
        create_res = self.client.post('/api/v1/reviews/', 
                                      data=json.dumps(self.valid_review_data),
                                      content_type='application/json')
        review_id = json.loads(create_res.data)['id']

        # Then fetch it
        get_res = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(json.loads(get_res.data)['id'], review_id)

    def test_update_review(self):
        """Test updating a review's text and rating"""
        # Create
        create_res = self.client.post('/api/v1/reviews/', 
                                      data=json.dumps(self.valid_review_data),
                                      content_type='application/json')
        review_id = json.loads(create_res.data)['id']

        # Update
        update_data = {"text": "Actually, it was just okay.", "rating": 3}
        put_res = self.client.put(f'/api/v1/reviews/{review_id}', 
                                  data=json.dumps(update_data),
                                  content_type='application/json')
        self.assertEqual(put_res.status_code, 200)

        # Verify Update
        verify_res = self.client.get(f'/api/v1/reviews/{review_id}')
        updated_data = json.loads(verify_res.data)
        self.assertEqual(updated_data['text'], "Actually, it was just okay.")
        self.assertEqual(updated_data['rating'], 3)

    def test_delete_review(self):
        """Test deleting a review"""
        # Create
        create_res = self.client.post('/api/v1/reviews/', 
                                      data=json.dumps(self.valid_review_data),
                                      content_type='application/json')
        review_id = json.loads(create_res.data)['id']

        # Delete
        del_res = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(del_res.status_code, 200)

        # Verify Deletion (This should definitely return 404 now!)
        verify_res = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(verify_res.status_code, 404)

    def test_get_reviews_by_place(self):
        """Test retrieving all reviews for a specific place"""
        # Create a review linked to self.place_id
        self.client.post('/api/v1/reviews/', 
                         data=json.dumps(self.valid_review_data),
                         content_type='application/json')

        # Fetch using the nested endpoint in places.py
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['text'], "Amazing experience!")

if __name__ == '__main__':
    unittest.main()