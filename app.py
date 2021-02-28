"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, default_url

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
    """currently redirects to users"""

    return redirect('/users')


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
    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


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
