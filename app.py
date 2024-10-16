from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route("/")
def main():
    return render_template("base.html")

@app.route("/homepage")
def home():
    #View for the Home page of your website.

    agent = request.user_agent

    return render_template("home.html", agent=agent)

@app.route("/hi/<string:name>") #/hi/roman?age=19
def greetings(name):
    name = name.upper()
    age = request.args.get("age", 0, int)

    return render_template("hi.html", name=name, age=age)

@app.route("/admin")
def admin():
    to_url = url_for("greetings", name = "administrotor", age = 19)
    return redirect(to_url)

posts = [
    {"id": 0, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 1, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 2, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
]

@app.route("/posts")
def get_posts():
    return render_template("posts.html", posts=posts)

@app.route("/post/<int:id>")
def detail_post(id):
    post = posts[id]
    return render_template("detail_post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)