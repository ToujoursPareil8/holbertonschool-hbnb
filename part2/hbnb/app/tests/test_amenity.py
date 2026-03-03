import unittest
from flask import json
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', 
                                    data=json.dumps({"name": "Wi-Fi"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['name'], "Wi-Fi")

    def test_get_amenities(self):
        self.client.post('/api/v1/amenities/', data=json.dumps({"name": "Pool"}), content_type='application/json')
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(json.loads(response.data)), 1)

if __name__ == '__main__':
    unittest.main()