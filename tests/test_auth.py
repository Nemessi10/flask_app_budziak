import unittest
from app import create_app, db
from app.users.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # Налаштовуємо тестову Flask аплікацію та базу даних
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        # Очищаємо базу даних після кожного тесту
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def test_register_page_load(self):
        """Тестуємо, чи правильно завантажується сторінка реєстрації."""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        #self.assertIn(b'Register', response.data)

    def test_login_page_load(self):
        """Тестуємо, чи правильно завантажується сторінка входу."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        """Тестуємо, чи зберігається користувач у базі даних після реєстрації."""
        response = self.client.get('/register')
        csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

        response = self.client.post('/register', data={
            'csrf_token': csrf_token,
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'confirm_password': 'password'
        })
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_user_login(self):
        """Тестуємо, чи користувач може увійти після реєстрації."""
        self.client.post('/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'confirm_password': 'password'
        })
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        """Тестуємо, чи користувач може вийти з системи."""
        self.client.post('/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'confirm_password': 'password'
        })
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password'
        })
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
