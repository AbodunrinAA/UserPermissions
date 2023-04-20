import unittest
import json
from app import app

class UserTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {'Content-Type': 'application/json'}
        
    def test_create_user(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'firstname': 'Test',
            'lastname': 'User',
            'dateofbirth': '01-01-1990'
        }
        response = self.app.post('/user', headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.json['message'])
        
    def test_create_user_with_existing_email(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'firstname': 'Test',
            'lastname': 'User',
            'dateofbirth': '1990-01-01'
        }
        response = self.app.post('/user', headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 400)
        self.assertIn('User with the same email already exists', response.json['message'])
        
    def test_get_user_by_email(self):
        response = self.app.get('/users/testuser@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'testuser@example.com')
        
    def test_get_user_by_email_not_found(self):
        response = self.app.get('/users/nonexistent@example.com')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Record not found', response.json['message'])
        
    def test_delete_user(self):
        response = self.app.delete('/users/testuser@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted successfully', response.json['message'])
        
    def test_delete_nonexistent_user(self):
        response = self.app.delete('/users/nonexistent@example.com')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.json['message'])
        
    def test_get_all_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        
    def test_get_users_by_lastname(self):
        response = self.app.get('/users/Lastname')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        
if __name__ == '__main__':
    unittest.main()
