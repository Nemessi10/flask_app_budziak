from flask import request, redirect, url_for, render_template, current_app

@current_app.route("/")
def main():
    return render_template("base.html")

