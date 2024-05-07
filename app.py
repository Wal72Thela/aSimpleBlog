import sqlite3
from flask import Flask,abort, render_template


def db_connection():
    connector = sqlite3.connect('database.db')
    connector.row_factory = sqlite3.Row
    return connector

def get_post(post_id):
    connector = db_connection()
    post = connector.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()

    connector.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)

@app.route("/")
def index():
    connector = db_connection()
    posts = connector.execute('SELECT * FROM posts').fetchall()
    connector.close()
    return render_template("index.html", posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html',post=post)


if __name__ == "__main__":
    app.run(debug=True)