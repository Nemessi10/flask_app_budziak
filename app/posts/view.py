import json

from flask import render_template, abort, flash, redirect, url_for, session
from app.posts import post_bp
from app.posts.forms import PostForm

posts = [
    {"id": 0, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 1, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 2, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
]

@post_bp.route("/")
def get_posts():
    posts_data = load_posts()
    return render_template("posts.html", posts=posts_data)

@post_bp.route("/<int:id>")
def detail_post(id):
    if id >= len(posts):
        abort(400)
    post = posts[id]
    return render_template("detail_post.html", post=post)

@post_bp.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        # Завантаження існуючих постів
        posts_data = load_posts()

        new_id = max([post['id'] for post in posts_data], default=-1) + 1

        # Додавання нового поста
        new_post = {
            "id": new_id,
            "title": form.title.data,
            "content": form.content.data,
            "is_active": form.is_active.data,
            "publish_date": form.publish_date.data.strftime('%Y-%m-%d'),
            "category": form.category.data,
            "author": session.get('username', 'Unknown')  # Автор з сесії
        }

        posts_data.append(new_post)

        # Збереження постів у JSON
        save_posts(posts_data)

        return redirect(url_for("posts.get_posts"))
    return render_template("add_post.html", form=form)

# Завантаження постів з JSON-файлу
def load_posts():
    try:
        with open("posts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Збереження постів у JSON-файл
def save_posts(posts_data):
    with open("posts.json", "w") as file:
        json.dump(posts_data, file, indent=4)