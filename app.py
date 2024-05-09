import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort




# configurations
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post(title='{self.title}', content='{self.content}')"





# routes

@app.route("/")
def index():
    posts = Post.query.all()
    print(posts)
    return render_template("index.html", posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            new_post = Post(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!')
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        if not post.title:
            flash('Title is required!')
        else:
            db.session.commit()
            flash('Post updated successfully!')
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)






with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True,port=8080)