from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta

from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.users import user_bp, auth_bp
from app.users.forms import RegistrationForm
from app.users.models import User

users_info = [
    {"username" : "admin", "password" : "admin"}
]

@user_bp.route("/profile")
@login_required
def get_profile():
    cookies = [
        [cookie, request.cookies[cookie]] for cookie in request.cookies if cookie != 'session'
    ]
    color_value = session.get("color", "default")
    return render_template("profile.html", username=current_user.username, cookies=cookies, color=color_value)

@user_bp.route("/change_colors", methods=["GET", "POST"])
def change_colors():
    if request.method == "POST":
        color = request.form["color"]
        session["color"] = color
        return redirect(url_for('users.get_profile'))
    return redirect(url_for('users.get_profile'))

@user_bp.route("/homepage")
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@user_bp.route("/hi/<string:name>") #/hi/roman?age=19
def greetings(name):
    name = name.upper()
    age = request.args.get("age", 0, int)

    return render_template("hi.html", name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name = "administrator", age = 19, _external=True)
    return redirect(to_url)

@user_bp.route("/resume")
def resume():
    return render_template("resume.html")

@user_bp.route("/list")
@login_required
def users_list():
    # Отримуємо усіх користувачів із бази даних
    users = User.query.all()

    if not users:
        # Якщо користувачів немає, відображаємо повідомлення
        return render_template('users_list.html', message="No users found.")

    # Якщо користувачі є, передаємо їх у шаблон
    return render_template('users_list.html', users=users, users_count=len(users))

@user_bp.route("/account")
@login_required
def account():
    # Перевірка, чи користувач авторизований
    if "username" not in session:
        flash("You need to log in first.", "danger")
        return redirect(url_for("auth.login"))  # Перенаправлення на сторінку входу

    # Отримання даних користувача з сесії
    username = session["username"]
    user = User.query.filter_by(username=username).first()

    return render_template("account.html", user=user)  # Передача даних користувача в шаблон


@user_bp.route("/set_cookie")
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', '', max_age=timedelta(seconds=60))
    return response

@user_bp.route("/get_cookie")
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@user_bp.route("/delete_cookie")
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response

@user_bp.route("/set_cookie_val", methods=["GET", "POST"])
def set_cookie_val():
    if request.method == "POST":
        key = request.form["cookie_key"]
        value = request.form["cookie_value"]
        duration = int(request.form["cookie_duration"])
        response = make_response(redirect(url_for('users.get_profile')))
        response.set_cookie(key, value, max_age=duration)
        return response
    return redirect(url_for('users.get_profile'))

@user_bp.route("/delete_cookie_by_key", methods=["GET", "POST"])
def delete_cookie_by_key():
    if request.method == "POST":
        key = request.form["cookie_key"]
        response = make_response(redirect(url_for('users.get_profile')))
        response.set_cookie(key, '', expires=0)
        return response
    return redirect(url_for('users.get_profile'))

@user_bp.route("/delete_all_cookies", methods=["GET", "POST"])
def delete_all_cookies():
    if request.method == "POST":
        response = make_response(redirect(url_for('users.get_profile')))
        for cookie in request.cookies:
            if cookie != 'session':
                response.delete_cookie(cookie)
        return response
    return redirect(url_for('users.get_profile'))

# auth
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("users.get_profile"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)  # Авторизація
            session["username"] = user.username
            flash("Login successful!", "success")
            return redirect(url_for("users.account"))
        flash("Invalid username or password.", "danger")

    return render_template("login.html")

@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))