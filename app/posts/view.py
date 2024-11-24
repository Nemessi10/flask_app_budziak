from flask import render_template, abort, redirect, url_for, session
from app.posts import post_bp
from app.posts.forms import PostForm
from app.posts.utils import load_posts, save_post, get_post


@post_bp.route("/")
def get_posts():
    posts_data = load_posts()  # Завантаження постів із JSON
    return render_template("posts.html", posts=posts_data)


@post_bp.route("/<int:id>")
def detail_post(id):
    post = get_post(id)  # Отримання конкретного поста
    if not post:
        abort(404)  # Повертаємо 404, якщо пост не знайдено
    return render_template("detail_post.html", post=post)


@post_bp.route("/new", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        # Генерація нового поста
        posts_data = load_posts()
        new_id = max([post['id'] for post in posts_data], default=-1) + 1

        new_post = {
            "id": new_id,
            "title": form.title.data,
            "content": form.content.data,
            "is_active": form.is_active.data,
            "publish_date": form.publish_date.data.strftime('%Y-%m-%d'),
            "category": form.category.data,
            "author": session.get('username', 'Unknown')  # Автор із сесії
        }

        save_post(new_post)  # Збереження нового поста
        return redirect(url_for("posts.get_posts"))

    return render_template("add_post.html", form=form)
