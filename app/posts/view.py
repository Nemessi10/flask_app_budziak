from flask import render_template, abort
from . import post_bp

posts = [
    {"id": 0, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 1, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 2, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
]

@post_bp.route("/")
def get_posts():
    return render_template("posts.html", posts=posts)

@post_bp.route("/<int:id>")
def detail_post(id):
    if id >= len(posts):
        abort(400)
    post = posts[id]
    return render_template("detail_post.html", post=post)