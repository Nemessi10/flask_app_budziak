from flask import render_template, url_for, redirect, request
from app.users import user_bp

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
