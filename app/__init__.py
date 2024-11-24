from flask import Flask, render_template

def create_app(config_name="config"):
    app = Flask(__name__)
    app.config.from_object(config_name)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        from . import view
        from .posts import post_bp
        from .users import user_bp
        app.register_blueprint(post_bp)
        app.register_blueprint(user_bp)

    return app
