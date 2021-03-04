"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, default_url, Post, Tag, PostTag
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "dogs4life"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def base():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)


@app.route('/users')
def list_users():
    """Lists all users"""
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def user_form():
    return render_template('new_user.html')


@app.route('/users/new', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = image_url if len(image_url) > 0 else None

    if len(first_name) < 3 or len(last_name) < 3:
        flash('First Name and Last Name must be at least 3 characters')
        return redirect('/users/new')

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    db.session.flush()
    user = User.query.get(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    user.image_url = user.image_url if len(user.image_url) > 0 else default_url

    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    db.session.flush()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def save_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")
    new_post = Post(title=title, content=content, user_id=user_id)

    for tag in tags:
        t = Tag.query.get(tag)
        new_post.tags.append(t)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    db.session.flush()
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = []

    tags = request.form.getlist("tags")

    for tag in tags:
        t = Tag.query.get(tag)
        post.tags.append(t)

    db.session.commit()
    return redirect(f"/posts/{post.id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    db.session.flush()
    post = Post.query.get(post_id)
    user_id = post.user.id

    post.tags = []

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route('/tags/new')
def tag_form():
    return render_template('new_tag.html')


@app.route('/tags/new', methods=["POST"])
def add_tag():
    name = request.form["name"]

    if len(name) < 3:
        flash('Tag must be at least 3 characters')
        return redirect('/tags/new')

    check_name = Tag.query.filter_by(name=name).all()

    if len(check_name) == 0:
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()

        return redirect("/tags")

    else:
        flash('That tag already exists')
        return redirect('/tags/new')


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    db.session.flush()
    tag = Tag.query.get(tag_id)
    tag.name = request.form["name"]

    db.session.commit()
    return redirect(f"/tags/{tag.id}")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    db.session.flush()

    tag = Tag.query.get(tag_id)

    tag.posts = []

    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect(f"/tags")
