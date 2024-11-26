from flask import render_template, abort, redirect, url_for, session, flash

from app import db
from app.posts import post_bp
from app.posts.forms import PostForm
from app.posts.models import Post

@post_bp.route("/")
def get_posts():
    posts_data = Post.query.order_by(Post.publish_date.desc()).all()  # Сортування за спаданням
    return render_template("posts.html", posts=posts_data)


@post_bp.route("/<int:id>")
def detail_post(id):
    post = Post.query.get(id)  # Отримуємо пост за ID з БД
    if not post:
        abort(404)  # Повертаємо 404, якщо пост не знайдено
    return render_template("detail_post.html", post=post)


@post_bp.route("/new", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            publish_date=form.publish_date.data,
            category=form.category.data,
            author=session.get("username", "Unknown")  # Автор із сесії
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("posts.get_posts"))

    return render_template("add_post.html", form=form)

@post_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.publish_date = form.publish_date.data
        post.category = form.category.data

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('posts.get_posts'))

    return render_template("edit_post.html", form=form, post=post)


@post_bp.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post {post.title} was successfully deleted!", "success")
    return redirect(url_for("posts.get_posts"))
