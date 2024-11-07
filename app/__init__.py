from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile("../config.py")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

from app import view

from app.posts import post_bp
from app.users import user_bp
app.register_blueprint(post_bp)
app.register_blueprint(user_bp)