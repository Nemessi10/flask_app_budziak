SECRET_KEY = "secret-key-password"
SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret-key-password"