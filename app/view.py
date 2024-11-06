from flask import request, redirect, url_for, render_template
from app import app

@app.route("/")
def main():
    return render_template("base.html")

