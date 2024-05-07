import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

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
app.config['SECRET-KEY'] = 'For now it works'

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


@app.route('/create', methods =('GET', 'POST'))
def create():
    if request.method == 'POST':
        # getting the title from the form 
        title = request.form['title']

        # getting content from the form
        content = request.form['content']

        if not title:
            flash('Title required!')
        else:
            connector = db_connection()
            connector.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connector.commit()
            connector.close()
            return redirect(url_for('index'))
    return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)