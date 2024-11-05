from flask import request, redirect, url_for, render_template
from app import app

@app.route("/")
def main():
    return render_template("base.html")

@app.route("/homepage")
def home():
    #View for the Home page of your website.

    agent = request.user_agent

    return render_template("home.html", agent=agent)
