from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


default_url = "https://media.istockphoto.com/vectors/man-vector-icon-gender-icon-vector-id1132067376?k=6&m=1132067376&s=612x612&w=0&h=BUCm8AwVk5yoZnW6M5JWy2NLbN93NwFL1Rm8n69pwvw="


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    image_url = db.Column(db.String(300), nullable=False,
                          default=default_url)

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False)

    content = db.Column(db.String(1000), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship('User', backref='posts')

    tags = db.relationship('Tag', secondary="post_tags",
                           backref="posts", cascade="delete")

    def __repr__(self):
        p = self
        return f"<id={p.id} title={p.title} content={p.content} user_id={p.user_id}>"


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(40), nullable=False, unique=True)

    def __repr__(self):
        t = self
        return f"<id={t.id} name={t.name}>"


class PostTag(db.Model):

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key="True")

    tag_id = db.Column(db.Integer, db.ForeignKey(
        "tags.id", ondelete="CASCADE"), primary_key="True")
