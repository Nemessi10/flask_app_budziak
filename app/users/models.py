from app import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def set_password(self, raw_password):
        """Хешування пароля перед збереженням."""
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        """Перевірка пароля на відповідність."""
        return bcrypt.check_password_hash(self.password, raw_password)

    @property
    def is_active(self):
        """Повертає True, якщо користувач активний."""
        return True  # Якщо вам не потрібно блокувати користувачів, це достатньо

    def __repr__(self):
        return f"<User {self.email}>"
