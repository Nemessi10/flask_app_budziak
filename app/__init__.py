from flask import Flask
app = Flask(__name__)
app.config.from_pyfile("../config.py")

from app import view

from app.posts import post_bp
from app.users import user_bp
app.register_blueprint(post_bp)
app.register_blueprint(user_bp)