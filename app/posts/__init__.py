from flask import Blueprint

post_bp = Blueprint(
    "posts",
    __name__,
    url_prefix = "/posts",
    template_folder = "templates",
    static_folder = "static",
    static_url_path = "/static_for_posts")

from app.posts import view