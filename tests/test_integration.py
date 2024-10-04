import unittest
import requests

class TestFlaskIntegration(unittest.TestCase):
    def test_hello_endpoint(self):
        response = requests.get('http://localhost:5005/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, World!', response.json()['message'])

if __name__ == '__main__':
    unittest.main()

