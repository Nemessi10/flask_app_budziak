import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        """Тест маршруту /user/hi/<name>."""
        response = self.client.get("/user/hi/Roman?age=19")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ROMAN", response.data)
        self.assertIn(b"19", response.data)

    def test_admin_page(self):
        """Тест маршруту /user/admin, який перенаправляє."""
        response = self.client.get("/user/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"19", response.data)

if __name__ == "__main__":
    unittest.main()
