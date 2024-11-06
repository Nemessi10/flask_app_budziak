from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta, datetime
from app.users import user_bp

users_info = [
    {"username" : "admin", "password" : "admin"}
]

@user_bp.route("/profile")
def get_profile():
    if "username" in session:
        cookies = []
        for cookie in request.cookies:
            if cookie != 'session':
                cookies.append([cookie, request.cookies[cookie]]) # ім'я, значення
        username_value = session["username"]
        color_value = session["color"]
        return render_template("profile.html", username=username_value, cookies=cookies, color=color_value)
    return redirect(url_for("users.login"))

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        for user in users_info:
            if username == user["username"] and password == user["password"]:
                session["username"] = username
                session["color"] = "success"
                flash("Success: logged in successfully.", "success")
                return redirect(url_for('users.get_profile'))
        flash("Warning: wrong login or password.", "danger")
    return render_template("login.html")

@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("age", None)
    return redirect(url_for('users.get_profile'))

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

@user_bp.route("/get_all_cookies")
def get_all_cookies():
    #cookies = request.cookies.get_dict()
    cookies = 0