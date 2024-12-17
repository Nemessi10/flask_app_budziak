from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

db = SQLAlchemy()
migrate = Migrate(model_class=Base)
bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.users.models import User
    return User.query.get(int(user_id))

def create_app(config_name="config"):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page"
    login_manager.login_message_category = "warning"

    from .users.models import User
    from .events.models import EventCategory, SportEvent

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        from app.users.view import login
        from . import view
        from .posts import post_bp
        from .users import user_bp, auth_bp
        from .events import events_bp
        app.register_blueprint(post_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(events_bp)

    return app
